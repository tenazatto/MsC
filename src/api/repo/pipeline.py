import json
import os
from datetime import datetime

from pipeline.processors.enums import UnbiasPostProcAlgorithms, UnbiasDataAlgorithms, Preprocessors, Datasets


class PipelineRepository:
    def get_dataset(self, dataset):
        indexes = {
            'Datasets.ADULT_INCOME': Datasets.ADULT_INCOME,
            'Datasets.GERMAN_CREDIT': Datasets.GERMAN_CREDIT
        }

        return next(filter(lambda a: a[0] == dataset, indexes.items()))[1]

    def get_preprocessor(self, preprocessor):
        indexes = {
            'Preprocessors.SEX': Preprocessors.SEX,
            'Preprocessors.AGE': Preprocessors.AGE,
            'Preprocessors.FOREIGN': Preprocessors.FOREIGN
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
                    'checksum': item['checksum'],
                    'date_start': item['date_start'],
                    'date_end': item['date_end'],
                    'execution_time_ms': item['execution_time_ms'],
                    'dataset': item['pipeline_params']['dataset'],
                    'preprocessor': item['pipeline_params']['preprocessor'],
                    'unbias_data_algorithm': item['pipeline_params']['unbias_data_algorithm'],
                    'algorithm': item['pipeline_params']['algorithm'],
                    'unbias_postproc_algorithm': item['pipeline_params']['unbias_postproc_algorithm'],
                    'metrics_summary': item['metrics_summary']
                },
                map(lambda item: json.load(open('output/metrics/' + item, 'r')), data)
            ),
            key=lambda item: datetime.strptime(item['date_start'], '%d/%m/%Y %H:%M:%S.%f'), reverse=True
        )[0]

        performance_metrics = list(filter(lambda x: 'accuracy' in x[0] or
                                                  'precision' in x[0] or
                                                  'recall' in x[0] or
                                                  'f1_score' in x[0] or
                                                  'auc' in x[0], data['metrics_summary'].items()))

        fairness_metrics = list(filter(lambda x: 'average_abs_odds_difference' in x[0] or
                                              'disparate_impact' in x[0] or
                                              'equal_opportunity_difference' in x[0] or
                                              'statistical_parity_difference' in x[0] or
                                              'theil_index' in x[0], data['metrics_summary'].items()))

        del data['metrics_summary']
        data['performance_metrics'] = dict(performance_metrics)
        data['fairness_metrics'] = dict(fairness_metrics)

        return data
