import json
import pandas as pd
import os
from datetime import datetime

from src.mapek.ml.analyzer import MLMAPEKExecutionAnalyzer, MLMAPEKPipelineAnalyzer
from src.mapek.ml.executor import MLMAPEKPipelineExecutor
from src.mapek.ml.monitor import MLMAPEKPipelineMonitor
from src.mapek.ml.planner import MLMAPEKDataChecksumPlanner, MLMAPEKAlgorithmValidationPlanner, \
    MLMAPEKPipelineThresholdPlanner, MLMAPEKPipelinePlanner
from src.mapek.orchestrator import MAPEKPipelineOrchestrator
from src.pipeline.pipeline import Pipeline
from src.pipeline.processors.enums import UnbiasPostProcAlgorithms, UnbiasDataAlgorithms, Preprocessors, Datasets


class PipelineRepository:
    def get_dataset(self, dataset):
        indexes = {
            'Datasets.ADULT_INCOME': Datasets.ADULT_INCOME,
            'Datasets.GERMAN_CREDIT': Datasets.GERMAN_CREDIT,
            'Datasets.LENDINGCLUB': Datasets.LENDINGCLUB,
        }

        return next(filter(lambda a: a[0] == dataset, indexes.items()))[1]

    def get_preprocessor(self, preprocessor):
        indexes = {
            'Preprocessors.SEX': Preprocessors.SEX,
            'Preprocessors.AGE': Preprocessors.AGE,
            'Preprocessors.FOREIGN': Preprocessors.FOREIGN,
            'Preprocessors.INCOME': Preprocessors.INCOME
        }

        return next(filter(lambda a: a[0] == preprocessor, indexes.items()))[1]

    def get_preproc_algorithm(self, algorithm):
        indexes = {
            'UnbiasDataAlgorithms.REWEIGHING': UnbiasDataAlgorithms.REWEIGHING,
            'UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING': UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING,
            'UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER': UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER,
            'UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS': UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS,
            'UnbiasDataAlgorithms.NOTHING': UnbiasDataAlgorithms.NOTHING
        }

        return next(filter(lambda a: a[0] == algorithm, indexes.items()))[1]

    def get_inproc_algorithm(self, algorithm):
        indexes = {
            'Algorithms.LOGISTIC_REGRESSION': 1,
            'Algorithms.RANDOM_FOREST': 2,
            'Algorithms.GRADIENT_BOOST': 3,
            'Algorithms.SUPPORT_VECTOR_MACHINES': 4,
            'Algorithms.LINEAR_REGRESSION': 901,
            'Algorithms.DECISION_TREE': 902,
            'Algorithms.KERNEL_RIDGE': 903,
            'Algorithms.NAIVE_BAYES': 5,
            'UnbiasInProcAlgorithms.PREJUDICE_REMOVER': 101,
            'UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING': 102,
            'UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION': 103,
            'UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS': 104,
            'UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION': 105,
            'UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER': 106,
            'UnbiasInProcAlgorithms.ART_CLASSIFIER': 107
        }

        return next(filter(lambda a: a[0] == algorithm, indexes.items()))[1]

    def get_postproc_algorithm(self, algorithm):
        indexes = {
            'UnbiasPostProcAlgorithms.EQUALIZED_ODDS': UnbiasPostProcAlgorithms.EQUALIZED_ODDS,
            'UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS': UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS,
            'UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION': UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION,
            'UnbiasPostProcAlgorithms.NOTHING': UnbiasPostProcAlgorithms.NOTHING
        }

        return next(filter(lambda a: a[0] == algorithm, indexes.items()))[1]

    def get_last_execution(self):
        data = os.listdir('output/metrics')
        data = sorted(
            map(
                lambda item: {
                    'file_id': item[0],
                    'data_checksum': item[1]['checksum'],
                    'date_start': item[1]['date_start'],
                    'date_end': item[1]['date_end'],
                    'execution_time_ms': item[1]['execution_time_ms'],
                    'dataset': item[1]['pipeline_params']['dataset'],
                    'preprocessor': item[1]['pipeline_params']['preprocessor'],
                    'unbias_data_algorithm': item[1]['pipeline_params']['unbias_data_algorithm'],
                    'inproc_algorithm': item[1]['pipeline_params']['algorithm'],
                    'unbias_postproc_algorithm': item[1]['pipeline_params']['unbias_postproc_algorithm'],
                    'metrics_summary': item[1]['metrics_summary']
                },
                map(lambda item: (item.replace('.json',''), json.load(open('output/metrics/' + item, 'r'))), data)
            ),
            key=lambda item: datetime.strptime(item['date_start'], '%d/%m/%Y %H:%M:%S.%f'), reverse=True
        )[0]

        metrics = list(
            map(
                lambda metric: {
                    'file_id': data['file_id'],
                    'data_checksum': data['data_checksum'],
                    'metric_id': metric[0],
                    'metric_name': metric[1]['name'],
                    'description': metric[1]['explanation'],
                    'value': metric[1]['value'][0] if type(metric[1]['value']) == list else metric[1]['value']
                },
                data['metrics_summary'].items()
            )
        )

        mapek = MAPEKPipelineOrchestrator(Pipeline(),
                                          MLMAPEKPipelineMonitor(),
                                          [MLMAPEKExecutionAnalyzer(), MLMAPEKPipelineAnalyzer()],
                                          [MLMAPEKDataChecksumPlanner(last_checksum=True),
                                           MLMAPEKAlgorithmValidationPlanner(), MLMAPEKPipelineThresholdPlanner(),
                                           MLMAPEKPipelinePlanner()],
                                          MLMAPEKPipelineExecutor())

        df_score = mapek.do_analyze(pd.DataFrame(metrics), pd.DataFrame([data]))

        self.put_metrics_and_score(data, df_score)

        return data

    def get_best_executions(self, pipeline_plan, df_score, num_best):
        data = {}
        data['pipelines'] = []

        for i in range(0, num_best):
            if len(pipeline_plan) > i:
                data['pipelines'].append(self.get_best_execution_item(df_score, pipeline_plan, i))

        return data

    def get_best_execution_item(self, df_score, pipeline_plan, index):
        pipeline_plan_dict = pipeline_plan.iloc[index].to_dict()
        df_score = df_score[
            (df_score['dataset'] == ('Datasets.' + pipeline_plan_dict['dataset'].name)) &
            (df_score['preprocessor'] == ('Preprocessors.' + pipeline_plan_dict['preprocessor'].name)) &
            (df_score['unbias_data_algorithm'] == (
                        'UnbiasDataAlgorithms.' + pipeline_plan_dict['unbias_data_algorithm'].name)) &
            (df_score['inproc_algorithm'] == pipeline_plan_dict['inproc_algorithm_name']) &
            (df_score['unbias_postproc_algorithm'] == (
                        'UnbiasPostProcAlgorithms.' + pipeline_plan_dict['unbias_postproc_algorithm'].name))
            ].reset_index()
        data = os.listdir('output/metrics')
        data = map(
            lambda item: {
                'file_id': item[0],
                'data_checksum': item[1]['checksum'],
                'date_start': item[1]['date_start'],
                'date_end': item[1]['date_end'],
                'execution_time_ms': item[1]['execution_time_ms'],
                'dataset': item[1]['pipeline_params']['dataset'],
                'preprocessor': item[1]['pipeline_params']['preprocessor'],
                'unbias_data_algorithm': item[1]['pipeline_params']['unbias_data_algorithm'],
                'inproc_algorithm': item[1]['pipeline_params']['algorithm'],
                'unbias_postproc_algorithm': item[1]['pipeline_params']['unbias_postproc_algorithm'],
                'metrics_summary': item[1]['metrics_summary']
            },
            map(lambda item: (item.replace('.json', ''), json.load(open('output/metrics/' + item, 'r'))), data)
        )
        filter_dict = df_score.iloc[0].to_dict()
        data = filter(lambda item: item['dataset'] == filter_dict['dataset'] and
                                   item['preprocessor'] == filter_dict['preprocessor'] and
                                   item['unbias_data_algorithm'] == filter_dict['unbias_data_algorithm'] and
                                   item['inproc_algorithm'] == filter_dict['inproc_algorithm'] and
                                   item['unbias_postproc_algorithm'] == filter_dict['unbias_postproc_algorithm'], data)
        data = sorted(
            data,
            key=lambda item: datetime.strptime(item['date_start'], '%d/%m/%Y %H:%M:%S.%f'), reverse=True
        )[0]
        self.put_metrics_and_score(data, df_score)
        return data

    def put_metrics_and_score(self, data, df_score):
        del data['file_id']
        performance_metrics = list(filter(lambda x: 'accuracy' == x[0] or
                                                    'precision' == x[0] or
                                                    'recall' == x[0] or
                                                    'f1_score' == x[0] or
                                                    'auc' == x[0], data['metrics_summary'].items()))
        fairness_metrics = list(filter(lambda x: 'average_abs_odds_difference' == x[0] or
                                                 'disparate_impact' == x[0] or
                                                 'equal_opportunity_difference' == x[0] or
                                                 'statistical_parity_difference' == x[0] or
                                                 'theil_index' == x[0], data['metrics_summary'].items()))
        del data['metrics_summary']
        data['performance_metrics'] = dict(performance_metrics)
        data['fairness_metrics'] = dict(fairness_metrics)
        data['scores'] = {
            'performance_score': int(df_score['standard_score'][0]),
            'fairness_score': int(df_score['fairness_score'][0]),
            'group_score': int(df_score['score'][0])
        }
