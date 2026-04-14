#!/usr/bin/env python3
"""
个人财务管理系统 - non-GSD模式 (单文件版本)
"""
import json
import os
import argparse
from datetime import date
import matplotlib.pyplot as plt
plt.switch_backend('Agg')

DATA_FILE = "finance_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'transactions': [], 'categories': []}
    return {'transactions': [], 'categories': [
        {'id': 1, 'name': '工资', 'type': 'income'},
        {'id': 2, 'name': '餐饮', 'type': 'expense'},
        {'id': 3, 'name': '交通', 'type': 'expense'}
    ]}


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_transaction(amount, type, description, category_id=None):
    data = load_data()
    t = {
        'id': len(data['transactions']) + 1,
        'amount': amount,
        'type': type,
        'category_id': category_id,
        'description': description,
        'date': str(date.today())
    }
    data['transactions'].append(t)
    save_data(data)
    print(f"Added: #{t['id']}")


def list_transactions():
    data = load_data()
    for t in data['transactions']:
        print(f"#{t['id']} | {t['date']} | {t['type']} | {t['amount']} | {t.get('description', '')}")


def delete_transaction(id):
    data = load_data()
    data['transactions'] = [t for t in data['transactions'] if t['id'] != id]
    save_data(data)
    print(f"Deleted #{id}")


def show_summary():
    data = load_data()
    income = sum(t['amount'] for t in data['transactions'] if t['type'] == 'income')
    expense = sum(t['amount'] for t in data['transactions'] if t['type'] == 'expense')
    print(f"Income: {income}")
    print(f"Expense: {expense}")
    print(f"Balance: {income - expense}")


def create_chart():
    data = load_data()
    income = sum(t['amount'] for t in data['transactions'] if t['type'] == 'income')
    expense = sum(t['amount'] for t in data['transactions'] if t['type'] == 'expense')
    plt.bar(['Income', 'Expense'], [income, expense], color=['green', 'red'])
    plt.savefig('chart.png')
    print("Chart saved to chart.png")


def main():
    parser = argparse.ArgumentParser(description="Personal Finance Manager")
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('amount', type=float)
    add_parser.add_argument('type', choices=['income', 'expense'])
    add_parser.add_argument('--description', default='')
    add_parser.add_argument('--category', type=int)

    list_parser = subparsers.add_parser('list')
    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('id', type=int)
    summary_parser = subparsers.add_parser('summary')
    chart_parser = subparsers.add_parser('chart')

    args = parser.parse_args()

    if args.command == 'add':
        add_transaction(args.amount, args.type, args.description, args.category)
    elif args.command == 'list':
        list_transactions()
    elif args.command == 'delete':
        delete_transaction(args.id)
    elif args.command == 'summary':
        show_summary()
    elif args.command == 'chart':
        create_chart()


if __name__ == '__main__':
    main()
