import json

import pandas as pd
from mapek.steps.planner import MAPEKPlanner
from pipeline.processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, UnbiasPostProcAlgorithms
from pipeline.validation import MAPEKValidation


class MLMAPEKPipelinePlanner(MAPEKPlanner):
    def plan(self, data):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)

        MAPEKValidation.validate_pipeline_planner_params(data)

        result = data.iloc[0]

        #TODO Realizar Assurance Cases
        #TODO Realizar Analyzer/Planner de acordo com Assurance Cases

        return pd.DataFrame([{
            'dataset': self.find_dataset(result['dataset']),
            'preprocessor': self.find_preprocessor(result['preprocessor']),
            'unbias_data_algorithm': self.find_preproc_algorithm(result['unbias_data_algorithm']),
            'inproc_algorithm_name': result['inproc_algorithm'],
            'inproc_algorithm': self.find_inproc_algorithm(result['inproc_algorithm']),
            'unbias_postproc_algorithm': self.find_postproc_algorithm(result['unbias_postproc_algorithm'])
        }])

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

    def plan(self, data):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)

        MAPEKValidation.validate_data_checksum_planner_params(self.checksum, self.last_checksum)

        if self.last_checksum:
            self.checksum = data.sort_values(by='last_date_end', ascending=False).iloc[0]['data_checksum']
            data = data[data['data_checksum'] == self.checksum]
            self.checksum = None
        else:
            data = data[data['data_checksum'] == self.checksum]

            #TODO Realizar Assurance Cases
        #TODO Realizar Analyzer/Planner de acordo com Assurance Cases

        return data


class MLMAPEKAlgorithmValidationPlanner(MAPEKPlanner):
    def plan(self, data):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)
        valid_algorithms = json.load(open('config/mapek/valid_algorithms.json', 'r'))
        df_valid = pd.DataFrame(valid_algorithms["valid_algorithms"],
                                columns=["inproc_algorithm", "unbias_data_algorithm", "unbias_postproc_algorithm"])

        return data.merge(df_valid)

class MLMAPEKAlgorithmPerformancePlanner(MAPEKPlanner):
    train_time = -1

    def __init__(self, train_time=-1):
        self.train_time = train_time

    def plan(self, data):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)

        return data if self.train_time < 0 else data[data['execution_time_ms'] < self.train_time]