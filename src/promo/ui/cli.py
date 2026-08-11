# src/promo/ui/cli.py


from promo.todo.service import TaskService
from promo.todo.task import Task


class CLI:

    def __init__(self, task_service:TaskService):
        self.task_service = task_service

    def run(self):
        command = input("Promo > ").strip().lower()
        self.dispatch(command)

    def dispatch(self, command):
        match command:
            case "add":
                self.add_task()

            case "list":
                print("List selected")

            case "delete":
                print("Delete selected")

            case _:
                print("Unknown command")

    def add_task(self):
        title = input("Title: ").strip()
        task = Task(title=title)
        self.task_service.add(task)
