from abc import ABC, abstractmethod


class MAPEKPlanner(ABC):
    def plan(self, data, enabled):
        if enabled:
            return self.do_plan(data)

        return data

    @abstractmethod
    def do_plan(self, data):
        pass
