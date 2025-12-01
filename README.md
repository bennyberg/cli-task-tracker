# Task CLI - Simple Task Tracker

Task CLI is a lightweight command-line tool for tracking your tasks directly from the terminal.
It lets you quickly add what you need to do, mark what you’re working on, and keep track of what’s already done - all stored locally in a simple JSON file.

## Features:

* Add new tasks with a short description

* Update the description of existing tasks

* Delete tasks you no longer need

* Mark tasks as todo, in-progress, or done

* List:

    * all tasks

    * only done tasks

    * only in-progress tasks

    * only todo tasks

* Tasks are stored in a tasks.json file in the current directory

## Example Usage:

### Add a new task
    task-cli add "Buy groceries"

### List all tasks
    task-cli list

### Mark a task as in progress
    task-cli mark-in-progress 1

### Mark a task as done
    task-cli mark-done 1

### List only done tasks
    task-cli list done

### Update a task description
    task-cli update 1 "Buy groceries and snacks"

### Delete a task
    task-cli delete 1

