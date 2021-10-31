from abc import abstractmethod, ABC


class MAPEKAnalyzer(ABC):
    @abstractmethod
    def analyze(self):
        pass
