import main
import pandas as pd

from api.repo.pipeline import PipelineRepository
from mapek.ml.analyzer import MLMAPEKExecutionAnalyzer, MLMAPEKPipelineAnalyzer
from mapek.ml.executor import MLMAPEKPipelineExecutor
from mapek.ml.monitor import MLMAPEKPipelineMonitor
from mapek.ml.planner import MLMAPEKDataChecksumPlanner, MLMAPEKAlgorithmValidationPlanner, \
    MLMAPEKPipelineThresholdPlanner, MLMAPEKPipelinePlanner
from mapek.orchestrator import MAPEKPipelineOrchestrator
from pipeline.pipeline import Pipeline


class PipelineService:
    pipeline_repository = PipelineRepository()

    def single_execution(self, request):
        main.execute_single(self.pipeline_repository.get_dataset(request['dataset']),
                            self.pipeline_repository.get_preprocessor(request['preprocessor']),
                            self.pipeline_repository.get_preproc_algorithm(request['preproc_algorithm']),
                            self.pipeline_repository.get_inproc_algorithm(request['inproc_algorithm']),
                            self.pipeline_repository.get_postproc_algorithm(request['postproc_algorithm']))

        return self.pipeline_repository.get_last_execution()

    def auto_execution(self, request):
        # main.mapek(self.pipeline_repository.get_dataset(request['dataset']))
        mapek = MAPEKPipelineOrchestrator(Pipeline(),
                                          MLMAPEKPipelineMonitor(),
                                          [MLMAPEKExecutionAnalyzer(), MLMAPEKPipelineAnalyzer()],
                                          [MLMAPEKDataChecksumPlanner(last_checksum=True),
                                           MLMAPEKAlgorithmValidationPlanner(), MLMAPEKPipelineThresholdPlanner(),
                                           MLMAPEKPipelinePlanner()],
                                          MLMAPEKPipelineExecutor())

        pipeline, metrics = mapek.monitor.monitor()
        df_score = mapek.do_analyze(pd.DataFrame(metrics), pd.DataFrame(pipeline))
        pipeline_plan = mapek.do_plan(df_score)

        return self.pipeline_repository.get_best_execution(pipeline_plan, df_score)
