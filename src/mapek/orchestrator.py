import json
import math
import re
from datetime import datetime
from typing import List

from mapek.steps.analyzer import MAPEKAnalyzer
from mapek.steps.executor import MAPEKExecutor
from mapek.steps.monitor import MAPEKMonitor
from mapek.steps.planner import MAPEKPlanner
from pipeline.pipeline import Pipeline


class MAPEKPipelineOrchestrator:
    monitor: MAPEKMonitor = None
    analyzers: List[MAPEKAnalyzer] = []
    planners: List[MAPEKPlanner] = []
    executor: MAPEKExecutor = None
    pipeline: Pipeline = None

    def __init__(self, pipeline: Pipeline,
                 monitor: MAPEKMonitor,
                 analyzers: List[MAPEKAnalyzer],
                 planners: List[MAPEKPlanner],
                 executor: MAPEKExecutor):
        self.pipeline = pipeline
        self.monitor = monitor
        self.analyzers = analyzers
        self.planners = planners
        self.executor = executor

    def run(self):
        while True:
            date_start = datetime.now()
            df_pipeline, df_metrics = self.monitor.monitor()

            planner_flags = json.load(open('config/mapek/planner_flags.json', 'r'))
            analyzer_flags = json.load(open('config/mapek/analyzer_flags.json', 'r'))

            df_score = None
            for analyzer in self.analyzers:
                prop = analyzer.__class__.__name__.replace('MAPEK', '').replace('Analyzer', '')
                prop = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', prop)
                prop = re.sub('([a-z0-9])([A-Z])', r'\1_\2', prop).lower()
                enabled = analyzer_flags[prop]

                df_analyzed = df_pipeline if df_score is None else df_score
                df_score = analyzer.analyze(data=(df_analyzed, df_metrics), enabled=enabled)

            pipeline_plan = None
            for planner in self.planners:
                prop = planner.__class__.__name__.replace('MAPEK', '').replace('Planner', '')
                prop = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', prop)
                prop = re.sub('([a-z0-9])([A-Z])', r'\1_\2', prop).lower()
                enabled = planner_flags[prop]

                pipeline_plan = df_score if pipeline_plan is None else pipeline_plan
                pipeline_plan = planner.plan(data=pipeline_plan, enabled=enabled)

            self.executor.execute(data=(self.pipeline, pipeline_plan))
            date_end = datetime.now()
            print('Execução realizada em ' + str(math.floor((date_end - date_start).total_seconds() * 1000)) + ' ms')

