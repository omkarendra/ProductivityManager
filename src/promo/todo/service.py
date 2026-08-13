# src/promo/todo/service.py

from build.lib.promo.todo import task
from promo.todo.category import Category
from promo.todo.category_repository import CategoryRepository
from promo.todo.repository import TaskRepository

VALID_STATUSES = {
    "pending",
    "in_progress",
    "completed"
}
class TaskService:

    def __init__(self, task_repository: TaskRepository, category_repository: CategoryRepository):
        self.task_repository = task_repository
        self.category_repository = category_repository

    def add(self, task):
        print (f"Adding task: {task.title}, Category: {task.category}, Status: {task.status}")
        if task.status is not None:
            if task.status not in VALID_STATUSES:
                raise ValueError(f"Invalid status: {task.status}")

        if task.category:
            category = self.get_or_create_category(task.category)
            task.category_id = category.id
        self.task_repository.save(task)
        
    def find_tasks(self, category=None):
        return self.task_repository.find(category)
    
    def delete(self, task_id: int):
        self.task_repository.delete(task_id)

    def get_or_create_category(self, name):
        category = self.category_repository.find_by_name(name)

        if category is not None: # Category exists
            return category

        category = Category(name)   # category does not exists
        self.category_repository.save(category)

        return category
    def update(self, task_id, title=None, description=None, category=None, status=None):
        task = self.task_repository.find_by_id(task_id)

        if task is None:
            raise ValueError(f"Task {task_id} not found")

        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        if category is not None:
            category_obj = self.get_or_create_category(category)
            task.category_id = category_obj.id
            task.category = category

        if status is not None:
            if status not in VALID_STATUSES:
                raise ValueError(f"Invalid status: {status}")

            task.status = status

        self.task_repository.update(task)