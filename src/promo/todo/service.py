# src/promo/todo/service.py

from promo.todo.category import Category
from promo.todo.category_repository import CategoryRepository
from promo.todo.repository import TaskRepository


class TaskService:

    def __init__(self, task_repository: TaskRepository, category_repository: CategoryRepository):
        self.task_repository = task_repository
        self.category_repository = category_repository

    def add(self, task):
        if task.category:
            category = self.get_or_create_category(task.category)
            task.category_id = category.id
        self.task_repository.save(task)
        
    def list(self):
        return self.task_repository.find_all()
    
    def delete(self, task_id: int):
        self.task_repository.delete(task_id)

    def get_or_create_category(self, name):
        category = self.category_repository.find_by_name(name)

        if category is not None: # Category exists
            return category

        category = Category(name)   # category does not exists
        self.category_repository.save(category)

        return category