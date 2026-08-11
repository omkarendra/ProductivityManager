# src/promo/todo/service.py

from promo.todo.repository import TaskRepository


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add(self, task):
        self.repository.save(task)
        
    def list(self):
        return self.repository.find_all()