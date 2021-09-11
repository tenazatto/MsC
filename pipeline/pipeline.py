from pipeline.validation import PipelineValidation
from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, Algorithms, UnbiasInProcAlgorithms
from processors.inprocessors.algorithms import logistic_regression_weighed, logistic_regression, prejudice_remover
from processors.preprocessors.data.adult_sex import AdultSexPreprocessor
from processors.preprocessors.data.german_age import GermanAgePreprocessor
from processors.preprocessors.data.german_foreign import GermanForeignPreprocessor
from processors.preprocessors.algorithms import reweighing_preprocess, optim_preprocess, disparate_impact_preprocess, \
    biased_explainer, \
    prejudice_remover_preprocess


class Pipeline:
    def select_data_preprocessor(self, dataset, preprocessor):
        if dataset == Datasets.ADULT_INCOME and preprocessor == Preprocessors.SEX:
            preprocessor = AdultSexPreprocessor()
        elif dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.AGE:
            preprocessor = GermanAgePreprocessor()
        elif dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.FOREIGN:
            preprocessor = GermanForeignPreprocessor()

        return preprocessor

    def unbias_data_preprocessor(self, params, algorithm, unbias_data_algorithm):
        x_train, x_test, y_train, y_test, preprocessor = params
        result = None

        if algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            dataset_tr, dataset_te, explainer = \
                prejudice_remover_preprocess(x_train, x_test, y_train, y_test, preprocessor)
            result = dataset_tr, dataset_te, y_test, explainer
        else:
            if unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING:
                df_aif_rw, unbiased_explainer = reweighing_preprocess(x_train, y_train, preprocessor)
                result = x_train, x_test, y_train, y_test, df_aif_rw, unbiased_explainer
            elif unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING:
                df_aif_op, unbiased_explainer = optim_preprocess(x_train, y_train, preprocessor)
                result = x_train, x_test, y_train, y_test, df_aif_op, unbiased_explainer
            elif unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
                x_di_train, x_di_test, y_di_train, unbiased_explainer = \
                    disparate_impact_preprocess(x_train, x_test, y_train, y_test, preprocessor)
                result = x_train, x_test, y_train, y_test, \
                       x_di_train, x_di_test, y_di_train, \
                       unbiased_explainer
            elif unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING:
                explainer = biased_explainer(x_train, y_train, preprocessor)
                result = x_train, x_test, y_train, y_test, explainer

        return result

    def data_preprocess(self, dataset, preprocessor, algorithm, unbias_data_algorithm):
        preprocessor = self.select_data_preprocessor(dataset, preprocessor)
        x_train, x_test, y_train, y_test = preprocessor.dataset_preprocess()

        params = x_train, x_test, y_train, y_test, preprocessor
        final_data = self.unbias_data_preprocessor(params, algorithm, unbias_data_algorithm)

        return final_data

    def process(self, params, algorithm, unbias_data_algorithm):
        if algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING:
            x_train, y_train, x_test, df_aif = params
            y_pred = logistic_regression_weighed(x_train, y_train, x_test, df_aif.instance_weights)
        elif algorithm == Algorithms.LOGISTIC_REGRESSION:
            x_train, y_train, x_test = params
            y_pred = logistic_regression(x_train, y_train, x_test)
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            dataset_tr, dataset_te = params
            y_pred = prejudice_remover(dataset_tr, dataset_te)

        return y_pred

    def start(self, dataset, preprocessor, algorithm, unbias_data_algorithm):
        PipelineValidation.validate_params(dataset, preprocessor, algorithm, unbias_data_algorithm)

        final_data = self.data_preprocess(dataset, preprocessor, algorithm, unbias_data_algorithm)

        if unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
            x_train, x_test, y_train, y_test, x_di_train, x_di_test, y_di_train, explainer = final_data
            params = x_di_train, y_di_train, x_di_test
        elif unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING or unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING:
            x_train, x_test, y_train, y_test, df_aif_rw, explainer = final_data
            params = x_train, y_train, x_test, df_aif_rw
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            dataset_tr, dataset_te, y_test, explainer = final_data
            params = dataset_tr, dataset_te
        else:
            x_train, x_test, y_train, y_test, explainer = final_data
            params = x_train, y_train, x_test

        y_pred = self.process(params, algorithm, unbias_data_algorithm)

        return y_pred, y_test, explainer
