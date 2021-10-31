from mapek.steps.analyzer import MAPEKAnalyzer
from mapek.steps.executor import MAPEKExecutor
from mapek.steps.monitor import MAPEKMonitor
from mapek.steps.planner import MAPEKPlanner
from pipeline.pipeline import Pipeline


class MAPEKPipelineOrchestrator:
    monitor: MAPEKMonitor = None
    analyzer: MAPEKAnalyzer = None
    planner: MAPEKPlanner = None
    executor: MAPEKExecutor = None
    pipeline: Pipeline = None

    def __init__(self, pipeline: Pipeline,
                 monitor: MAPEKMonitor,
                 analyzer: MAPEKAnalyzer,
                 planner: MAPEKPlanner,
                 executor: MAPEKExecutor):
        self.pipeline = pipeline
        self.monitor = monitor
        self.analyzer = analyzer
        self.planner = planner
        self.executor = executor

    def run(self):
        while True:
            self.monitor.monitor()
            self.analyzer.analyze()
            self.planner.plan()

            self.executor.execute()

