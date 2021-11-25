from abc import ABC, abstractmethod


class MAPEKPlanner(ABC):
    @abstractmethod
    def plan(self, data):
        pass