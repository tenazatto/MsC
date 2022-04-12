from abc import abstractmethod, ABC


class MAPEKMonitor(ABC):
    @abstractmethod
    def monitor(self, filters=None):
        pass
