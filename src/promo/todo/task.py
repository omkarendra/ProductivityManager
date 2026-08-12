
class Task:
    def __init__(self, title, description=None,category=None, category_id=None, status=None, task_id=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.category_id = category_id
        self.status = status