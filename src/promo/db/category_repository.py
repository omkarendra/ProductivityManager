import sqlite3

from promo.todo.category import Category
from promo.todo.category_repository import CategoryRepository


class SQLiteCategoryRepository(CategoryRepository):

    def __init__(self, database_path):
        self.database_path = database_path

    def save(self, category):
        connection = sqlite3.connect(self.database_path)

        cursor = connection.execute(
            """
            INSERT INTO categories (name)
            VALUES (?)
            """,
            (category.name,)
        )

        category.id = cursor.lastrowid

        connection.commit()
        connection.close()

    def find_by_name(self, name):
        connection = sqlite3.connect(self.database_path)

        row = connection.execute(
            """
            SELECT id, name
            FROM categories
            WHERE name = ?
            """,
            (name,)
        ).fetchone()

        connection.close()

        if row is None:
            return None

        return Category(
            name=row[1],
            category_id=row[0]
        )

    def find_all(self):
        connection = sqlite3.connect(self.database_path)

        rows = connection.execute(
            """
            SELECT id, name
            FROM categories
            ORDER BY name
            """
        ).fetchall()

        connection.close()

        return [
            Category(
                name=row[1],
                category_id=row[0]
            )
            for row in rows
        ]