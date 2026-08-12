'''
    This file only contains methods that alter the schema of DB.
    Operations on existing tables are part of task_repository.
'''

import sqlite3

class Database:

    def __init__(self, database_path):
        self.database_path = database_path

    def initialize(self):
        connection = sqlite3.connect(self.database_path)
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category_id INTEGER,
                status TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
            """
        )

        connection.commit()
        connection.close()
