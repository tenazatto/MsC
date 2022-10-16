from src.mapek.ml.analyzer import MLMAPEKExecutionAnalyzer, MLMAPEKPipelineAnalyzer
from src.mapek.ml.executor import MLMAPEKPipelineExecutor
from src.mapek.ml.monitor import MLMAPEKPipelineMonitor
from src.mapek.ml.planner import MLMAPEKPipelinePlanner, MLMAPEKAlgorithmValidationPlanner, MLMAPEKDataChecksumPlanner, \
    MLMAPEKPipelineThresholdPlanner
from src.mapek.orchestrator import MAPEKPipelineOrchestrator

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
