'''
    This class with taskservice illustrate dependency inversion principle. 
    Taskservice depends on database service, but to keep them two loosely coupled, 
    Taskrepository is created. Taskservices only knows about TaskRepository. 
    TaskRepository can be implemented by any type of persistance. 
    Thus, TaskService is no loner coupled with any specific implementation of persistance.
'''


from abc import ABC, abstractmethod
from promo.todo.task import Task

class TaskRepository(ABC):

    @abstractmethod
    def save(self, task: Task):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def delete(self, task_id: int):
        pass