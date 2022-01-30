import pandas as pd
from mapek.steps.planner import MAPEKPlanner
from pipeline.processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, UnbiasPostProcAlgorithms


class MLMAPEKPipelinePlanner(MAPEKPlanner):
    def plan(self, data):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)
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

class MLMAPEKLastChecksumPlanner(MAPEKPlanner):
    def plan(self, data):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)
        result = data.iloc[0]

        #TODO Realizar Assurance Cases
        #TODO Realizar Analyzer/Planner de acordo com Assurance Cases

        return pd.DataFrame([{
            'dataset': result['dataset'],
            'preprocessor': result['preprocessor'],
            'unbias_data_algorithm': result['unbias_data_algorithm'],
            'inproc_algorithm': result['inproc_algorithm'],
            'unbias_postproc_algorithm': result['unbias_postproc_algorithm']
        }])

class MLMAPEKAlgorithmValidationPlanner(MAPEKPlanner):
    def plan(self, data):
        print('Efetuando estratégia de planejamento ' + self.__class__.__name__)
        result = data.iloc[0]

        #TODO Realizar Assurance Cases
        #TODO Realizar Analyzer/Planner de acordo com Assurance Cases

        return pd.DataFrame([{
            'dataset': result['dataset'],
            'preprocessor': result['preprocessor'],
            'unbias_data_algorithm': result['unbias_data_algorithm'],
            'inproc_algorithm': result['inproc_algorithm'],
            'unbias_postproc_algorithm': result['unbias_postproc_algorithm']
        }])
