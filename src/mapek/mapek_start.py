from mapek.ml.analyzer import MLMAPEKExecutionAnalyzer, MLMAPEKPipelineAnalyzer
from mapek.ml.executor import MLMAPEKPipelineExecutor
from mapek.ml.monitor import MLMAPEKPipelineMonitor
from mapek.ml.planner import MLMAPEKPipelinePlanner, MLMAPEKAlgorithmValidationPlanner, MLMAPEKDataChecksumPlanner, \
    MLMAPEKPipelineThresholdPlanner
from mapek.orchestrator import MAPEKPipelineOrchestrator

from src.pipeline.pipeline import Pipeline


def mapek(dataset=None):
    mapek = MAPEKPipelineOrchestrator(Pipeline(),
                                      MLMAPEKPipelineMonitor(),
                                      [MLMAPEKExecutionAnalyzer(), MLMAPEKPipelineAnalyzer()],
                                      [MLMAPEKDataChecksumPlanner(last_checksum=True), MLMAPEKAlgorithmValidationPlanner(), MLMAPEKPipelineThresholdPlanner(), MLMAPEKPipelinePlanner()],
                                      MLMAPEKPipelineExecutor())
    print("Executando MAPE-K")
    mapek.run(dataset=dataset)


if __name__ == '__main__':
    mapek()
