#!/usr/bin/env python3
"""
个人财务管理系统 - GSD模式 (修复版)
"""
import os
import csv
import json
import argparse
import sqlite3
from datetime import datetime, date
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Category:
    id: int
    name: str
    type: TransactionType


@dataclass
class Transaction:
    amount: float = 0.0
    type: TransactionType = TransactionType.EXPENSE
    description: str = ""
    date: str = field(default_factory=lambda: date.today().isoformat())
    id: Optional[int] = None
    category_id: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Budget:
    category_id: int
    monthly_limit: float = 0.0
    month: str = ""
    id: Optional[int] = None
    spent: float = 0.0


class Database:
    def __init__(self, db_path: str = "finance.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                type TEXT NOT NULL,
                category_id INTEGER,
                description TEXT,
                date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                monthly_limit REAL NOT NULL,
                month TEXT NOT NULL,
                spent REAL DEFAULT 0,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')

        self._insert_default_categories(cursor)
        conn.commit()
        conn.close()

    def _insert_default_categories(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            default_categories = [
                ("工资", "income"),
                ("奖金", "income"),
                ("餐饮", "expense"),
                ("交通", "expense"),
                ("购物", "expense"),
                ("娱乐", "expense"),
                ("房租", "expense"),
                ("医疗", "expense")
            ]
            cursor.executemany(
                "INSERT INTO categories (name, type) VALUES (?, ?)",
                default_categories
            )

    def get_connection(self):
        return sqlite3.connect(self.db_path)


class FinanceManager:
    def __init__(self, db: Database):
        self.db = db

    def add_transaction(self, transaction: Transaction) -> Transaction:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (amount, type, category_id, description, date, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (transaction.amount, transaction.type.value, transaction.category_id,
              transaction.description, transaction.date, transaction.created_at))
        transaction.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return transaction

    def get_transactions(self, start_date: str = None, end_date: str = None) -> List[Transaction]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = "SELECT id, amount, type, category_id, description, date, created_at FROM transactions"
        params = []
        if start_date and end_date:
            query += " WHERE date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [Transaction(id=r[0], amount=r[1], type=TransactionType(r[2]),
                           category_id=r[3], description=r[4], date=r[5], created_at=r[6])
                for r in rows]

    def delete_transaction(self, transaction_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def get_categories(self) -> List[Category]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, type FROM categories")
        rows = cursor.fetchall()
        conn.close()
        return [Category(id=r[0], name=r[1], type=TransactionType(r[2])) for r in rows]

    def get_summary(self, month: str = None) -> Dict[str, Any]:
        if not month:
            month = date.today().strftime("%Y-%m")
        start_date = f"{month}-01"
        end_date = f"{month}-31"
        transactions = self.get_transactions(start_date, end_date)

        income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
        expense = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)

        return {
            "month": month,
            "income": income,
            "expense": expense,
            "balance": income - expense,
            "transaction_count": len(transactions)
        }

    def export_csv(self, filename: str, transactions: List[Transaction] = None):
        if transactions is None:
            transactions = self.get_transactions()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "金额", "类型", "分类ID", "描述", "日期", "创建时间"])
            for t in transactions:
                writer.writerow([t.id, t.amount, t.type.value, t.category_id,
                                 t.description, t.date, t.created_at])

    def import_csv(self, filename: str) -> int:
        imported = 0
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = Transaction(
                    amount=float(row['金额']),
                    type=TransactionType(row['类型']),
                    category_id=int(row['分类ID']) if row.get('分类ID') else None,
                    description=row.get('描述', ''),
                    date=row.get('日期', date.today().isoformat())
                )
                self.add_transaction(t)
                imported += 1
        return imported

    def create_chart(self, month: str, output_file: str = "report.png"):
        summary = self.get_summary(month)
        transactions = self.get_transactions(f"{month}-01", f"{month}-31")

        categories = {}
        for t in transactions:
            if t.type == TransactionType.EXPENSE:
                cat_id = t.category_id or 0
                if cat_id not in categories:
                    categories[cat_id] = 0
                categories[cat_id] += t.amount

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.bar(['收入', '支出'], [summary['income'], summary['expense']],
                color=['green', 'red'])
        ax1.set_title(f'{month} 收支对比')
        ax1.set_ylabel('金额')

        if categories:
            ax2.pie(categories.values(), labels=[f'分类{k}' for k in categories.keys()],
                    autopct='%1.1f%%')
            ax2.set_title('支出分类占比')

        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()


def main():
    parser = argparse.ArgumentParser(description="个人财务管理系统")
    subparsers = parser.add_subparsers(dest='command', required=True)

    add_parser = subparsers.add_parser('add', help='添加交易记录')
    add_parser.add_argument('amount', type=float, help='金额')
    add_parser.add_argument('type', choices=['income', 'expense'], help='类型')
    add_parser.add_argument('--category', type=int, help='分类ID')
    add_parser.add_argument('--description', default='', help='描述')
    add_parser.add_argument('--date', help='日期 (YYYY-MM-DD)')

    list_parser = subparsers.add_parser('list', help='列出交易记录')
    list_parser.add_argument('--start', help='开始日期')
    list_parser.add_argument('--end', help='结束日期')

    delete_parser = subparsers.add_parser('delete', help='删除交易记录')
    delete_parser.add_argument('id', type=int, help='交易ID')

    summary_parser = subparsers.add_parser('summary', help='查看月度总结')
    summary_parser.add_argument('--month', help='月份 (YYYY-MM)')

    categories_parser = subparsers.add_parser('categories', help='列出分类')

    export_parser = subparsers.add_parser('export', help='导出CSV')
    export_parser.add_argument('filename', help='输出文件名')

    import_parser = subparsers.add_parser('import', help='导入CSV')
    import_parser.add_argument('filename', help='输入文件名')

    chart_parser = subparsers.add_parser('chart', help='生成图表')
    chart_parser.add_argument('--month', help='月份 (YYYY-MM)')
    chart_parser.add_argument('--output', default='report.png', help='输出文件')

    args = parser.parse_args()
    db = Database()
    manager = FinanceManager(db)

    if args.command == 'add':
        t = Transaction(
            amount=args.amount,
            type=TransactionType(args.type),
            category_id=args.category,
            description=args.description,
            date=args.date or date.today().isoformat()
        )
        t = manager.add_transaction(t)
        print(f"已添加交易记录: #{t.id}")

    elif args.command == 'list':
        transactions = manager.get_transactions(args.start, args.end)
        for t in transactions:
            print(f"#{t.id} | {t.date} | {t.type.value:7} | {t.amount:10.2f} | {t.description}")

    elif args.command == 'delete':
        if manager.delete_transaction(args.id):
            print(f"已删除交易记录 #{args.id}")
        else:
            print(f"未找到交易记录 #{args.id}")

    elif args.command == 'summary':
        summary = manager.get_summary(args.month)
        print(f"=== {summary['month']} 月度总结 ===")
        print(f"收入: {summary['income']:.2f}")
        print(f"支出: {summary['expense']:.2f}")
        print(f"结余: {summary['balance']:.2f}")
        print(f"交易笔数: {summary['transaction_count']}")

    elif args.command == 'categories':
        categories = manager.get_categories()
        for c in categories:
            print(f"#{c.id} | {c.type.value:7} | {c.name}")

    elif args.command == 'export':
        manager.export_csv(args.filename)
        print(f"已导出到 {args.filename}")

    elif args.command == 'import':
        count = manager.import_csv(args.filename)
        print(f"已导入 {count} 条记录")

    elif args.command == 'chart':
        manager.create_chart(args.month, args.output)
        print(f"图表已保存到 {args.output}")


if __name__ == '__main__':
    main()
