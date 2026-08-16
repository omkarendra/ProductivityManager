import sqlite3
import pytest

from promo.db.task_repository import SQLiteTaskRepository
from promo.todo.task import Task


@pytest.fixture
def database(tmp_path):
    db_path = tmp_path / "test.db"

    connection = sqlite3.connect(db_path)

    connection.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    connection.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            status TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    connection.commit()
    connection.close()

    return str(db_path)

def test_save_task(database):
    repository = SQLiteTaskRepository(database)

    task = Task(
        title="Learn Git",
        status="pending"
    )

    repository.save(task)

    connection = sqlite3.connect(database)

    record = connection.execute(
        "SELECT title, status FROM tasks"
    ).fetchone()

    connection.close()

    assert record == ("Learn Git", "pending")


def test_find_task_by_id(database):
    repository = SQLiteTaskRepository(database)

    task = Task(
        title="Learn Git",
        description="Study branches",
        status="pending"
    )

    repository.save(task)

    found_task = repository.find_by_id(1)

    assert found_task is not None
    assert found_task.id == 1
    assert found_task.title == "Learn Git"
    assert found_task.description == "Study branches"
    assert found_task.status == "pending"    