from promo.db.category_repository import SQLiteCategoryRepository
from promo.db.database import Database
from promo.db.task_repository import SQLiteTaskRepository
from promo.todo.category import Category
from promo.todo.service import TaskService
from promo.todo.task import Task
from promo.ui.cli import CLI

def init_db(db_path):
    database = Database(db_path)
    database.initialize()
    
def main():
    db_path = "data/promo.db"

    init_db(db_path)

    task_repository = SQLiteTaskRepository(db_path)
    category_repository = SQLiteCategoryRepository(db_path)

    service = TaskService(
        task_repository,
        category_repository
    )

    cli = CLI(service)
    cli.run()



if __name__ == "__main__":
    main()
