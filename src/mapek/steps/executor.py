from abc import ABC, abstractmethod


class MAPEKExecutor(ABC):
    @abstractmethod
    def execute(self, data):
        pass
