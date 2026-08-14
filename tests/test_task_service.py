from promo.todo.service import TaskService
from promo.todo.task import Task
from promo.todo.category import Category


class FakeTaskRepository:
    def __init__(self):
        self.saved_task = None

    def save(self, task):
        self.saved_task = task


class FakeCategoryRepository:
    def __init__(self):
        self.categories = []

    def find_by_name(self, name):
        for category in self.categories:
            if category.name == name:
                return category

        return None

    def save(self, category):
        category.id = len(self.categories) + 1
        self.categories.append(category)

def test_add_task_creates_category():
    task_repository = FakeTaskRepository()
    category_repository = FakeCategoryRepository()

    service = TaskService(
        task_repository,
        category_repository
    )

    task = Task(
        "Learn Git",
        category="Research"
    )

    service.add(task)

    assert task.category_id == 1
    assert task_repository.saved_task is task

def test_add_task_reuses_existing_category():
    task_repository = FakeTaskRepository()
    category_repository = FakeCategoryRepository()

    existing_category = Category("Research")
    category_repository.save(existing_category)

    service = TaskService(
        task_repository,
        category_repository
    )

    task = Task(
        "Read paper",
        category="Research"
    )

    service.add(task)

    assert task.category_id == existing_category.id
    assert len(category_repository.categories) == 1