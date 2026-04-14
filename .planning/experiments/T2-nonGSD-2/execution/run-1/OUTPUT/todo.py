#!/usr/bin/env python3
"""
命令行待办事项管理工具 - non-GSD模式 (第二次重复)
"""
import json
import os
import argparse

DATA_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(t['id'] for t in tasks) + 1


def add_task(description, priority="medium"):
    tasks = load_tasks()
    task = {'id': get_next_id(tasks), 'description': description,
            'priority': priority, 'completed': False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task: #{task['id']} {description}")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) < len(tasks):
        save_tasks(new_tasks)
        print(f"Deleted task #{task_id}")
    else:
        print(f"Task #{task_id} not found")


def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            print(f"Completed task #{task_id}: {task['description']}")
            return
    print(f"Task #{task_id} not found")


def list_tasks(sort_by_priority=False):
    tasks = load_tasks()
    if sort_by_priority:
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        tasks.sort(key=lambda t: priority_order.get(t['priority'], 1))
    for task in tasks:
        status = "✓" if task['completed'] else "○"
        print(f"{status} #{task['id']} [{task['priority']}] {task['description']}")


def main():
    parser = argparse.ArgumentParser(description="Todo List CLI")
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a task')
    add_parser.add_argument('description', help='Task description')
    add_parser.add_argument('priority', nargs='?', default='medium',
                            choices=['low', 'medium', 'high'])

    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID')

    complete_parser = subparsers.add_parser('complete', help='Mark task complete')
    complete_parser.add_argument('id', type=int, help='Task ID')

    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--sort', choices=['priority'], help='Sort by priority')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description, args.priority)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'complete':
        complete_task(args.id)
    elif args.command == 'list':
        list_tasks(args.sort == 'priority')


if __name__ == '__main__':
    main()
