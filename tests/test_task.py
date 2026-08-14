from promo.todo.task import Task


def test_task_defaults_to_pending():
    task = Task("Learn Git")

    assert task.status == "pending"


def test_task_accepts_explicit_status():
    task = Task("Learn Git", status="completed")

    assert task.status == "completed"