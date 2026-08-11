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
        connection = sqlite3.connect(self.database_path)

        records = connection.execute(
            "SELECT id, title, description, category, status FROM tasks"
        ).fetchall()

        connection.close()
        return [
                Task(
                    title=row[1],
                    description=row[2],
                    category=row[3],
                    status=row[4],
                    task_id=row[0]
                )
                for row in records
            ]

    def delete(self, task_id: int):
        pass