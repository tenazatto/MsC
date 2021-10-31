from abc import abstractmethod, ABC


class MAPEKMonitor(ABC):
    @abstractmethod
    def monitor(self):
        pass
