import pandas as pd

from src.api.repo.pipeline import PipelineRepository
from src.mapek.ml.analyzer import MLMAPEKExecutionAnalyzer, MLMAPEKPipelineAnalyzer
from src.mapek.ml.executor import MLMAPEKPipelineExecutor
from src.mapek.ml.monitor import MLMAPEKPipelineMonitor
from src.mapek.ml.planner import MLMAPEKDataChecksumPlanner, MLMAPEKAlgorithmValidationPlanner, \
    MLMAPEKPipelineThresholdPlanner, MLMAPEKPipelinePlanner
from src.mapek.orchestrator import MAPEKPipelineOrchestrator
from src.pipeline.pipeline import Pipeline


class PipelineService:
    pipeline_repository = PipelineRepository()

    def single_execution(self, request):
        pipe = Pipeline()
        pipe.start(self.pipeline_repository.get_dataset(request['dataset']),
                   self.pipeline_repository.get_preprocessor(request['preprocessor']),
                   self.pipeline_repository.get_inproc_algorithm(request['inproc_algorithm']),
                   self.pipeline_repository.get_preproc_algorithm(request['preproc_algorithm']),
                   self.pipeline_repository.get_postproc_algorithm(request['postproc_algorithm']))

        return self.pipeline_repository.get_last_execution()

    def auto_execution(self, num_pipelines, dataset, preprocessor):
        mapek = MAPEKPipelineOrchestrator(Pipeline(),
                                          MLMAPEKPipelineMonitor(),
                                          [MLMAPEKExecutionAnalyzer(), MLMAPEKPipelineAnalyzer()],
                                          [MLMAPEKDataChecksumPlanner(last_checksum=True),
                                           MLMAPEKAlgorithmValidationPlanner(), MLMAPEKPipelineThresholdPlanner(),
                                           MLMAPEKPipelinePlanner()],
                                          MLMAPEKPipelineExecutor())

        filters = {}
        filters['dataset'] = self.pipeline_repository.get_dataset(dataset)
        if preprocessor != '':
            filters['preprocessor'] = self.pipeline_repository.get_preprocessor(preprocessor)

        pipeline, metrics = mapek.monitor.monitor(filters=filters)
        df_score = mapek.do_analyze(pd.DataFrame(metrics), pd.DataFrame(pipeline))
        pipeline_plan = mapek.do_plan(df_score, num_pipelines=num_pipelines)

        return self.pipeline_repository.get_best_executions(pipeline_plan, df_score, num_pipelines)
