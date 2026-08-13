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

    def find_by_id(self, task_id):
        connection = sqlite3.connect(self.database_path)

        record = connection.execute(
            """
            SELECT
                tasks.id,
                tasks.title,
                tasks.description,
                categories.name,
                tasks.category_id,
                tasks.status
            FROM tasks
            LEFT JOIN categories
                ON tasks.category_id = categories.id
            WHERE tasks.id = ?
            """,
            (task_id,)
        ).fetchone()

        connection.close()

        if record is None:
            return None

        return Task(
            title=record[1],
            description=record[2],
            category=record[3],
            category_id=record[4],
            status=record[5],
            task_id=record[0]
        )

    def find(self, category=None):
        connection = sqlite3.connect(self.database_path)

        query = """
            SELECT
                tasks.id,
                tasks.title,
                tasks.description,
                categories.name,
                tasks.status
            FROM tasks
            LEFT JOIN categories
                ON tasks.category_id = categories.id
        """

        parameters = []

        if category is not None:
            query += " WHERE categories.name = ?"
            parameters.append(category)

        records = connection.execute(
            query,
            parameters
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