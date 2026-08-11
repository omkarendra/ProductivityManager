import sqlite3

from promo.todo.repository import TaskRepository
from promo.todo.task import Task


class SQLiteTaskRepository(TaskRepository):

    def __init__(self, database_path):
        self.database_path = database_path

    def save(self, task: Task):
        connection = sqlite3.connect(self.database_path)

        connection.execute(
            """
            INSERT INTO tasks (title)
            VALUES (?)
            """,
            (task.title,)
        )

        connection.commit()
        connection.close()

    def find_all(self):
        pass

    def delete(self, task_id: int):
        pass