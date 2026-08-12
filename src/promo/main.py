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
    
def category_test(db_path):
    category = Category("Research")

    category_repository = SQLiteCategoryRepository(db_path)
    category_repository.save(category)

    print(category.id)

    found = category_repository.find_by_name("Research")
    print(found.id, found.name)

def main():
    #cli = CLI()
    #cli.run()
    db_path = "data/promo.db"
    init_db(db_path)
   
    #repository = SQLiteTaskRepository(db_path)
    #service = TaskService(repository)

    #cli = CLI(service)
    #cli.run()
    category_test(db_path)


if __name__ == "__main__":
    main()
