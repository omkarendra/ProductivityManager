
from abc import ABC, abstractmethod


class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category):
        pass

    @abstractmethod
    def find_by_name(self, name):
        pass

    @abstractmethod
    def find_all(self):
        pass