from promo.db.database import Database
from promo.db.task_repository import SQLiteTaskRepository
from promo.todo.service import TaskService
from promo.todo.task import Task
from promo.ui.cli import CLI

def init_db(db_path):
    database = Database(db_path)
    database.initialize()
    
def main():
    #cli = CLI()
    #cli.run()
    db_path = "data/promo.db"
    init_db(db_path)
   
    repo  = SQLiteTaskRepository(db_path)
    service =TaskService(repo)
    task = Task("test task")
    service.add(task)

    cli = CLI(service)
    cli.run()


if __name__ == "__main__":
    main()
