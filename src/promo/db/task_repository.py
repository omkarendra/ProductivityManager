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
            INSERT INTO tasks (
            title, description, category_id, status)
            VALUES (?, ?, ?, ?)
            """,
            (task.title, task.description, task.category_id, task.status)
        )

        connection.commit()
        connection.close()

    def find_all(self):
        connection = sqlite3.connect(self.database_path)

        records = connection.execute(
            """
            SELECT tasks.id, tasks.title, tasks.description, categories.name, tasks.status
            FROM tasks
            LEFT JOIN categories
                ON tasks.category_id = categories.id
            """
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
        connection = sqlite3.connect(self.database_path)

        connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        connection.commit()
        connection.close()