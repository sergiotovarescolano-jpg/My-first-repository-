"""
Simple Task Manager
--------------------
A small command-line tool to add, list, and complete tasks.
Tasks are saved locally in a JSON file so they persist between runs.
"""

import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(description):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "description": description,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {description}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet. Add one with: python task_manager.py add \"Your task\"")
        return
    for task in tasks:
        status = "✔" if task["done"] else " "
        print(f"[{status}] #{task['id']} {task['description']}")


def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Marked task #{task_id} as done.")
            return
    print(f"Task #{task_id} not found.")


def print_help():
    print("Usage:")
    print("  python task_manager.py add \"Task description\"")
    print("  python task_manager.py list")
    print("  python task_manager.py done <task_id>")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]

    if command == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif command == "list":
        list_tasks()
    elif command == "done" and len(sys.argv) > 2:
        try:
            complete_task(int(sys.argv[2]))
        except ValueError:
            print("Task id must be a number.")
    else:
        print_help()


if __name__ == "__main__":
    main()
