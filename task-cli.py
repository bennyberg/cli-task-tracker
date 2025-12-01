import sys
import os
import json
from datetime import datetime

TASKS_FILE = "tasks.json"
VALID_STATUSES = ("todo", "in-progress", "done")

# ========== JSON FILE HELPERS ==========
def load_tasks():
    """Load tasks from tasks.json. If file doesn't exist, return empty list."""

    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: tasks.json is not valid JSON. Fix or delete the file.")
        sys.exit(1)

    if not isinstance(data, list):
        print("Error: tasks.json format is invalid (expected a list).")
        sys.exit(1)

    return data


def save_tasks(tasks):
    """Save list of tasks to tasks.json."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def get_next_id(tasks):
    """Return next numeric id based on current tasks."""
    if not tasks:
        return 1
    # assume each task has an "id" key
    max_id = max(task.get("id", 0) for task in tasks)
    return max_id + 1

def find_task_by_id(tasks, task_id):
    """Return (task, index) pair or (None, None) if not found."""
    for i, t in enumerate(tasks):
        if t.get("id") == task_id:
            return t, i
    return None, None


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


# ========== task-cli helper functions ==========
def _change_status(task_id_str, new_status):
    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Error: <id> must be an integer.")
        return

    tasks = load_tasks()
    task, idx = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Error: No task with id {task_id}")
        return

    task["status"] = new_status
    task["updatedAt"] = now_iso()
    tasks[idx] = task
    save_tasks(tasks)

    print(f"Task {task_id} marked as {new_status}")

# ========== task-cli functions ==========
def print_help():
    """For use when calling task-cli without input"""

    print("Usage:")
    print("  task-cli add <description>")
    print("  task-cli update <id> <new-description>")
    print("  task-cli delete <id>")
    print("  task-cli mark-in-progress <id>")
    print("  task-cli mark-done <id>")
    print("  task-cli list [status]   # status: todo | in-progress | done")


def cmd_add(args):
    if not args:
        print("Error: description is required for 'add'")
        return

    description = " ".join(args)
    tasks = load_tasks()
    new_id = get_next_id(tasks)

    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Added task {new_id}: {description}")


def cmd_update(args):
    if len(args) < 2:
        print("Error: 'update' requires <id> and <new-description>")
        return
    task_id_str = args[0]
    new_description = " ".join(args[1:])
    if len(args) < 2:
        print("Error: 'update' requires <id> and <new-description>")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print("Error: <id> must be an integer.")
        return
    
    new_description = " ".join(args[1:])

    tasks = load_tasks()
    task, idx = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Error: No task with id {task_id}")
        return

    task["description"] = new_description
    task["updatedAt"] = now_iso()
    tasks[idx] = task

    save_tasks(tasks)
    print(f"Updated task {task_id}: {new_description}")


def cmd_delete(args):
    if len(args) != 1:
        print("Error: 'delete' requires exactly one <id>")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print("Error: <id> must be an integer.")
        return

    tasks = load_tasks()
    original_len = len(tasks)
    tasks = [t for t in tasks if t.get("id") != task_id]

    if len(tasks) == original_len:
        print(f"Error: No task with id {task_id}")
        return

    save_tasks(tasks)
    print(f"Deleted task {task_id}")

def cmd_mark_in_progress(args):
    if len(args) != 1:
        print("Error: 'mark-in-progress' requires exactly one <id>")
        return
    _change_status(args[0], "in-progress")

def cmd_mark_done(args):
    if len(args) != 1:
        print("Error: 'mark-done' requires exactly one <id>")
        return
    _change_status(args[0], "done")
    
def cmd_list(args):
    status = args[0] if args else None
    if status is not None and status not in VALID_STATUSES:
        print("Error: status must be one of:", ", ".join(VALID_STATUSES))
        return
    tasks = load_tasks()

    if status:
        tasks = [t for t in tasks if t.get("status") == status]

    if not tasks:
        print("No tasks found.")
        return

    for t in tasks:
        tid = t.get("id")
        st = t.get("status")
        desc = t.get("description")
        print(f"[{tid}] ({st}) {desc}")


COMMANDS = {
    "add": cmd_add,
    "update": cmd_update,
    "delete": cmd_delete,
    "mark-in-progress": cmd_mark_in_progress,
    "mark-done": cmd_mark_done,
    "list": cmd_list,
}


def main():
    args = sys.argv[1:]
    if not args:
        print_help()
        return

    command = args[0]
    command_args = args[1:]

    handler = COMMANDS.get(command)
    if handler is None:
        print(f"Unknown command: {command}")
        print_help()
        return

    handler(command_args)


if __name__ == "__main__":
    main()
