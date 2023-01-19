import json

import pandas as pd
from src.mapek.steps.planner import MAPEKPlanner
from src.pipeline.processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, UnbiasPostProcAlgorithms
from src.pipeline.validation import MAPEKValidation


class MLMAPEKPipelinePlanner(MAPEKPlanner):
    def do_plan(self, data, num_pipelines=0):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)

        MAPEKValidation.validate_pipeline_planner_params(data)

        if num_pipelines == 0:
            result = data.sort_values(by='score', ascending=False).iloc[0]

            return pd.DataFrame([{
                'dataset': self.find_dataset(result['dataset']),
                'preprocessor': self.find_preprocessor(result['preprocessor']),
                'unbias_data_algorithm': self.find_preproc_algorithm(result['unbias_data_algorithm']),
                'inproc_algorithm_name': result['inproc_algorithm'],
                'inproc_algorithm': self.find_inproc_algorithm(result['inproc_algorithm']),
                'unbias_postproc_algorithm': self.find_postproc_algorithm(result['unbias_postproc_algorithm'])
            }])
        else:
            result = data.sort_values(by='score', ascending=False).head(num_pipelines).reset_index().transpose().to_dict().items()

            result = list(
                map(lambda item : {
                    'dataset': self.find_dataset(item[1]['dataset']),
                    'preprocessor': self.find_preprocessor(item[1]['preprocessor']),
                    'unbias_data_algorithm': self.find_preproc_algorithm(item[1]['unbias_data_algorithm']),
                    'inproc_algorithm_name': item[1]['inproc_algorithm'],
                    'inproc_algorithm': self.find_inproc_algorithm(item[1]['inproc_algorithm']),
                    'unbias_postproc_algorithm': self.find_postproc_algorithm(item[1]['unbias_postproc_algorithm'])
                }, result)
            )

            return pd.DataFrame(result)

    def find_dataset(self, dataset):
        return Datasets.getByName(dataset.split('.')[1])

    def find_preprocessor(self, preprocessor):
        return Preprocessors.getByName(preprocessor.split('.')[1])

    def find_preproc_algorithm(self, algorithm):
        return UnbiasDataAlgorithms.getByName(algorithm.split('.')[1])

    def find_inproc_algorithm(self, algorithm):
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

    def find_postproc_algorithm(self, algorithm):
        return UnbiasPostProcAlgorithms.getByName(algorithm.split('.')[1])


class MLMAPEKDataChecksumPlanner(MAPEKPlanner):
    last_checksum = False
    checksum = None

    def __init__(self, checksum=None, last_checksum=False):
        self.checksum = checksum
        self.last_checksum = last_checksum

    def do_plan(self, data, num_pipelines=0):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)

        MAPEKValidation.validate_data_checksum_planner_params(self.checksum, self.last_checksum)

        if self.last_checksum:
            self.checksum = data.sort_values(by='last_date_end', ascending=False).iloc[0]['data_checksum']
            data = data[data['data_checksum'] == self.checksum]
            self.checksum = None
        else:
            data = data[data['data_checksum'] == self.checksum]

        return data


class MLMAPEKAlgorithmValidationPlanner(MAPEKPlanner):
    def do_plan(self, data, num_pipelines=0):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)
        valid_algorithms = json.load(open('config/mapek/valid_algorithms.json', 'r'))
        df_valid = pd.DataFrame(valid_algorithms["valid_algorithms"],
                                columns=["inproc_algorithm", "unbias_data_algorithm", "unbias_postproc_algorithm"])

        return data.merge(df_valid)


class MLMAPEKPipelineThresholdPlanner(MAPEKPlanner):
    def do_plan(self, data, num_pipelines=0):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)
        score_threshold = json.load(open('config/mapek/score_threshold.json', 'r'))

        return data[(data['score'] >= score_threshold['min_score']) & (data['score'] <= score_threshold['max_score'])]

