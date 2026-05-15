# To-Do List CLI Application

A simple command-line to-do list manager built with Python. This application uses `argparse` for handling CLI commands and JSON for persistent task storage.

## Features

- **Add tasks**: Create new to-do items with optional descriptions
- **List tasks**: View all pending tasks or all tasks including completed ones
- **Mark complete**: Mark tasks as done
- **Delete tasks**: Remove tasks from your list
- **JSON persistence**: Tasks are automatically saved to `tasks.json`

## Project Structure

```
.
├── src/
│   └── todo.py          # Main CLI application
├── tasks.json           # Task storage (auto-created)
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Installation

1. Ensure you have Python 3.7 or higher installed
2. Install dependencies (none required for basic functionality):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Add a task
```bash
python src/todo.py add "Buy groceries" --description "Milk, eggs, bread"
```

### List tasks
```bash
# Show only pending tasks
python src/todo.py list

# Show all tasks including completed
python src/todo.py list --all
```

### Mark a task as complete
```bash
python src/todo.py complete 1
```

### Delete a task
```bash
python src/todo.py delete 1
```

## Command Reference

| Command | Arguments | Description |
|---------|-----------|-------------|
| `add` | `TITLE` `[--description TEXT]` | Add a new task |
| `list` | `[--all]` | List pending tasks (or all if `--all` is used) |
| `complete` | `TASK_ID` | Mark a task as completed |
| `delete` | `TASK_ID` | Delete a task |

## Task Format

Tasks are stored in JSON format with the following structure:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-05-15T10:30:00.123456"
}
```

## Requirements

- Python 3.7+
- No external dependencies