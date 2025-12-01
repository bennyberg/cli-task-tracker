#!/usr/bin/env python3
import sys


def print_help():
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
    print(f"[DEBUG] Would add task: {description}")


def cmd_update(args):
    if len(args) < 2:
        print("Error: 'update' requires <id> and <new-description>")
        return
    task_id_str = args[0]
    new_description = " ".join(args[1:])
    print(f"[DEBUG] Would update task {task_id_str} to: {new_description}")


def cmd_delete(args):
    if len(args) != 1:
        print("Error: 'delete' requires exactly one <id>")
        return
    task_id_str = args[0]
    print(f"[DEBUG] Would delete task {task_id_str}")


def cmd_mark_in_progress(args):
    if len(args) != 1:
        print("Error: 'mark-in-progress' requires exactly one <id>")
        return
    task_id_str = args[0]
    print(f"[DEBUG] Would mark task {task_id_str} as in-progress")


def cmd_mark_done(args):
    if len(args) != 1:
        print("Error: 'mark-done' requires exactly one <id>")
        return
    task_id_str = args[0]
    print(f"[DEBUG] Would mark task {task_id_str} as done")


def cmd_list(args):
    status = args[0] if args else None
    if status not in (None, "todo", "in-progress", "done"):
        print("Error: status must be one of: todo, in-progress, done")
        return
    print(f"[DEBUG] Would list tasks with status: {status or 'ANY'}")


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
