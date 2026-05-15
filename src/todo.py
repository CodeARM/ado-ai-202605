#!/usr/bin/env python3
"""
Simple To-Do List CLI Application
Manages tasks using JSON storage with argparse for command-line interface.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


class TodoApp:
    """A simple to-do list application with JSON persistence."""

    def __init__(self, tasks_file: str = "tasks.json"):
        """Initialize the TodoApp with a JSON storage file."""
        self.tasks_file = Path(tasks_file)
        self.tasks = self._load_tasks()

    def _load_tasks(self) -> list:
        """Load tasks from JSON file."""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: tasks.json is corrupted. Starting fresh.")
                return []
        return []

    def _save_tasks(self) -> None:
        """Save tasks to JSON file."""
        with open(self.tasks_file, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, title: str, description: str = "") -> None:
        """Add a new task to the to-do list."""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": datetime.now().isoformat(),
        }
        self.tasks.append(task)
        self._save_tasks()
        print(f"✓ Task added: {title}")

    def list_tasks(self, show_completed: bool = False) -> None:
        """List all tasks, optionally filtering by completion status."""
        if not self.tasks:
            print("No tasks found.")
            return

        filtered_tasks = self.tasks
        if not show_completed:
            filtered_tasks = [t for t in self.tasks if not t["completed"]]

        if not filtered_tasks:
            print("No tasks to display.")
            return

        print("\nTo-Do List:")
        print("-" * 60)
        for task in filtered_tasks:
            status = "✓" if task["completed"] else "○"
            print(f"{status} [{task['id']}] {task['title']}")
            if task["description"]:
                print(f"    → {task['description']}")
        print("-" * 60)
        print(f"Total: {len(filtered_tasks)} task(s)\n")

    def complete_task(self, task_id: int) -> None:
        """Mark a task as completed."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self._save_tasks()
                print(f"✓ Task {task_id} marked as completed: {task['title']}")
                return
        print(f"Error: Task {task_id} not found.")

    def delete_task(self, task_id: int) -> None:
        """Delete a task from the to-do list."""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted_title = task["title"]
                self.tasks.pop(i)
                self._save_tasks()
                print(f"✓ Task {task_id} deleted: {deleted_title}")
                return
        print(f"Error: Task {task_id} not found.")


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="A simple to-do list CLI application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python todo.py add "Buy groceries" --description "Milk, eggs, bread"
  python todo.py list
  python todo.py list --all
  python todo.py complete 1
  python todo.py delete 1
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "--description", "-d", default="", help="Task description (optional)"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--all", action="store_true", help="Show completed tasks as well"
    )

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to complete")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

    args = parser.parse_args()

    # Create app instance
    app = TodoApp()

    # Execute commands
    if args.command == "add":
        app.add_task(args.title, args.description)
    elif args.command == "list":
        app.list_tasks(show_completed=args.all)
    elif args.command == "complete":
        app.complete_task(args.task_id)
    elif args.command == "delete":
        app.delete_task(args.task_id)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
