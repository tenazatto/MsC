from abc import abstractmethod, ABC


class MAPEKAnalyzer(ABC):
    def analyze(self, data, enabled):
        if enabled:
            return self.do_analysis(data)

        return data

    @abstractmethod
    def do_analysis(self, data):
        pass
