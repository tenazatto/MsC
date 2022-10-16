import json
import math
import re
from datetime import datetime
from typing import List

from src.mapek.steps.analyzer import MAPEKAnalyzer
from src.mapek.steps.executor import MAPEKExecutor
from src.mapek.steps.monitor import MAPEKMonitor
from src.mapek.steps.planner import MAPEKPlanner
from src.pipeline.pipeline import Pipeline


class MAPEKPipelineOrchestrator:
    monitor: MAPEKMonitor = None
    analyzers: List[MAPEKAnalyzer] = []
    planners: List[MAPEKPlanner] = []
    executor: MAPEKExecutor = None
    pipeline: Pipeline = None
    filters = None

    def __init__(self, pipeline: Pipeline,
                 monitor: MAPEKMonitor,
                 analyzers: List[MAPEKAnalyzer],
                 planners: List[MAPEKPlanner],
                 executor: MAPEKExecutor,
                 filters=None):
        self.pipeline = pipeline
        self.monitor = monitor
        self.analyzers = analyzers
        self.planners = planners
        self.executor = executor
        self.filters = filters

    def run(self, executions=0, dataset=None, preprocessor=None):
        infinite_execs = executions < 1
        num_executions = 0

        while infinite_execs or num_executions < executions:
            date_start = datetime.now()
            filters = self.build_filters(dataset, preprocessor)

            df_pipeline, df_metrics = self.monitor.monitor(filters=filters)

            df_score = self.do_analyze(df_metrics, df_pipeline)

            pipeline_plan = self.do_plan(df_score)

            self.executor.execute(data=(self.pipeline, pipeline_plan))
            date_end = datetime.now()
            print('Execução realizada em ' + str(math.floor((date_end - date_start).total_seconds() * 1000)) + ' ms')

    def build_filters(self, dataset, preprocessor):
        filters = {} if dataset is not None or preprocessor is not None else None
        if dataset is not None:
            filters['dataset'] = dataset
        if preprocessor is not None:
            filters['preprocessor'] = preprocessor
        return filters

    def do_analyze(self, df_metrics, df_pipeline):
        analyzer_flags = json.load(open('config/mapek/analyzer_flags.json', 'r'))
        df_score = None
        for analyzer in self.analyzers:
            prop = self.get_flag_name(analyzer, 'Analyzer')
            enabled = analyzer_flags[prop]

            df_analyzed = df_pipeline if df_score is None else df_score
            df_score = analyzer.analyze(data=(df_analyzed, df_metrics), enabled=enabled)
        return df_score

    def do_plan(self, df_score, num_pipelines=0):
        planner_flags = json.load(open('config/mapek/planner_flags.json', 'r'))
        pipeline_plan = None
        for planner in self.planners:
            prop = self.get_flag_name(planner, 'Planner')
            enabled = planner_flags[prop]

            pipeline_plan = df_score if pipeline_plan is None else pipeline_plan
            pipeline_plan = planner.plan(data=pipeline_plan, enabled=enabled, num_pipelines=num_pipelines)
        return pipeline_plan

    def get_flag_name(self, obj, type):
        prop = obj.__class__.__name__.replace('MAPEK', '').replace(type, '')
        prop = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', prop)
        prop = re.sub('([a-z0-9])([A-Z])', r'\1_\2', prop).lower()
        return prop
