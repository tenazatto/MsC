from abc import ABC, abstractmethod


class MAPEKPlanner(ABC):
    def plan(self, data, enabled, num_pipelines):
        if enabled:
            return self.do_plan(data, num_pipelines=num_pipelines)

        return data

    @abstractmethod
    def do_plan(self, data, num_pipelines=0):
        pass
