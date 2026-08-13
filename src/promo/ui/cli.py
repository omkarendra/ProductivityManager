# src/promo/ui/cli.py

import argparse
from promo.todo.service import TaskService
from promo.todo.task import Task


class CLI:

    def __init__(self, task_service:TaskService):
        self.task_service = task_service

    def run(self):
        parser = argparse.ArgumentParser(
            prog="promo",
            description="Personal productivity task manager"
        )

        subparsers = parser.add_subparsers(
            dest="command",
            required=True
        )

        add_parser = subparsers.add_parser( "add", help="Add a new task")
        list_parser = subparsers.add_parser("list", help="List tasks")

        add_parser.add_argument("-t", "--title", required=True, help="Task title")
        add_parser.add_argument("-d", "--description", help="Task description")
        add_parser.add_argument("-c", "--category", help="Task category")
        add_parser.add_argument("-s", "--status", help="Task status")

        list_parser.add_argument("-c", "--category", help="Filter tasks by category")

        args = parser.parse_args()

        if args.command == "add":
            self.add_task(args)
        elif args.command == "list":
            self.list_tasks(args)

    def list_tasks(self, args):
        tasks = self.task_service.list(args.category)

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            print( 
                f"{task.id}: "
                f"{task.title} | "
                f"{task.category} | "
                f"{task.status}"
            )

    def add_task(self, args):
        task = Task(
            title=args.title,
            description=args.description,
            category=args.category,
            status=args.status
        )

        self.task_service.add(task)

        print(f"Task added: {task.title}")

        
    # def dispatch(self, command):
    #     match command:
    #         case "add":
    #             self.add_task()

    #         case "list":
    #             self.list_tasks()

    #         case "delete":
    #             self.delete_task()

    #         case _:
    #             print("Unknown command")

    # def add_task(self):
    #     title = input("Title: ").strip()
    #     task = Task(title=title)
    #     self.task_service.add(task)

    # def list_tasks(self):
    #     tasks = self.task_service.list()

    #     for task in tasks:
    #         print(f"{task.id}: {task.title}")

    # def delete_task(self):
    #     task_id = int(input("Task ID: "))
    #     self.task_service.delete(task_id)