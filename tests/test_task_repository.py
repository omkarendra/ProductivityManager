from asyncio import tasks
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


def test_find_tasks_by_category(database):
    repository = SQLiteTaskRepository(database)

    connection = sqlite3.connect(database)

    connection.execute(
        "INSERT INTO categories (name) VALUES (?)",
        ("Research",)
    )
    connection.execute(
        "INSERT INTO categories (name) VALUES (?)",
        ("Teaching",)
    )

    connection.commit()

    research_id = connection.execute(
        "SELECT id FROM categories WHERE name = ?",
        ("Research",)
    ).fetchone()[0]

    teaching_id = connection.execute(
        "SELECT id FROM categories WHERE name = ?",
        ("Teaching",)
    ).fetchone()[0]

    connection.close()

    repository.save(
        Task(
            title="Read paper",
            category_id=research_id,
            status="pending"
        )
    )

    repository.save(
        Task(
            title="Prepare lecture",
            category_id=teaching_id,
            status="pending"
        )
    )

    research_tasks = repository.find("Research")

    assert len(research_tasks) == 1
    assert research_tasks[0].title == "Read paper"
    assert research_tasks[0].category == "Research"

    repository.find()

def test_find_all_tasks(database):
    repository = SQLiteTaskRepository(database)

    connection = sqlite3.connect(database)

    connection.execute(
        "INSERT INTO categories (name) VALUES (?)",
        ("Research",)
    )
    connection.execute(
        "INSERT INTO categories (name) VALUES (?)",
        ("Teaching",)
    )

    connection.commit()

    research_id = connection.execute(
        "SELECT id FROM categories WHERE name = ?",
        ("Research",)
    ).fetchone()[0]

    teaching_id = connection.execute(
        "SELECT id FROM categories WHERE name = ?",
        ("Teaching",)
    ).fetchone()[0]

    connection.close()

    repository.save(
        Task(
            title="Read paper",
            category_id=research_id,
            status="pending"
        )
    )

    repository.save(
        Task(
            title="Prepare lecture",
            category_id=teaching_id,
            status="completed"
        )
    )

    tasks = repository.find()

    assert len(tasks) == 2
    assert len(tasks) == 2

    titles = {task.title for task in tasks}

    assert titles == {"Read paper", "Prepare lecture" }

def test_update_task(database):
    repository = SQLiteTaskRepository(database)

    task = Task(
        title="Old title",
        description="Old description",
        status="pending"
    )

    repository.save(task)

    task.title = "New title"
    task.description = "New description"
    task.status = "completed"

    repository.update(task)

    updated_task = repository.find_by_id(task.id)

    assert updated_task is not None
    assert updated_task.title == "New title"
    assert updated_task.description == "New description"
    assert updated_task.status == "completed"


def test_delete_task(database):
    repository = SQLiteTaskRepository(database)

    task = Task(
        title="Task to delete",
        status="pending"
    )

    repository.save(task)

    repository.delete(task.id)

    deleted_task = repository.find_by_id(task.id)

    assert deleted_task is None