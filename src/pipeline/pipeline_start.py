import argparse

from src.pipeline.pipeline import Pipeline
from src.pipeline.processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, UnbiasInProcAlgorithms, Algorithms, \
    UnbiasPostProcAlgorithms


def execute_all():
    parser = argparse.ArgumentParser(description="Execuções de pipeline para determinado dataset")
    parser.add_argument("--dataset", help="Conjunto de dados tratado com atributo protegido",
                        choices=['ADULT_INCOME_SEX',
                                 'GERMAN_CREDIT_FOREIGN', 'GERMAN_CREDIT_AGE',
                                 'LENDINGCLUB_INCOME'])
    args = parser.parse_args()

    pipe = Pipeline()
    datasets = []

    process_options = [
        (Algorithms.LOGISTIC_REGRESSION, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.LOGISTIC_REGRESSION, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.EQUALIZED_ODDS),
        (Algorithms.LOGISTIC_REGRESSION, UnbiasDataAlgorithms.NOTHING,
         UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS),
        (Algorithms.LOGISTIC_REGRESSION, UnbiasDataAlgorithms.NOTHING,
         UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION),
        (Algorithms.LOGISTIC_REGRESSION, UnbiasDataAlgorithms.REWEIGHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.LOGISTIC_REGRESSION, UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER,
         UnbiasPostProcAlgorithms.NOTHING),
        # (Algorithms.LOGISTIC_REGRESSION, UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.LOGISTIC_REGRESSION, UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS,
         UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.RANDOM_FOREST, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.RANDOM_FOREST, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.EQUALIZED_ODDS),
        (Algorithms.RANDOM_FOREST, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS),
        (Algorithms.RANDOM_FOREST, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION),
        (Algorithms.RANDOM_FOREST, UnbiasDataAlgorithms.REWEIGHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.RANDOM_FOREST, UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER, UnbiasPostProcAlgorithms.NOTHING),
        # (Algorithms.RANDOM_FOREST, UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.RANDOM_FOREST, UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.GRADIENT_BOOST, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.GRADIENT_BOOST, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.EQUALIZED_ODDS),
        (Algorithms.GRADIENT_BOOST, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS),
        (Algorithms.GRADIENT_BOOST, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION),
        (Algorithms.GRADIENT_BOOST, UnbiasDataAlgorithms.REWEIGHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.GRADIENT_BOOST, UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER, UnbiasPostProcAlgorithms.NOTHING),
        # (Algorithms.GRADIENT_BOOST, UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.GRADIENT_BOOST, UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS,
         UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.NAIVE_BAYES, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.NAIVE_BAYES, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.EQUALIZED_ODDS),
        (Algorithms.NAIVE_BAYES, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS),
        (Algorithms.NAIVE_BAYES, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION),
        (Algorithms.NAIVE_BAYES, UnbiasDataAlgorithms.REWEIGHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.NAIVE_BAYES, UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER, UnbiasPostProcAlgorithms.NOTHING),
        # (Algorithms.GRADIENT_BOOST, UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.NAIVE_BAYES, UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS,
         UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.SUPPORT_VECTOR_MACHINES, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.SUPPORT_VECTOR_MACHINES, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.EQUALIZED_ODDS),
        (Algorithms.SUPPORT_VECTOR_MACHINES, UnbiasDataAlgorithms.NOTHING,
         UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS),
        (Algorithms.SUPPORT_VECTOR_MACHINES, UnbiasDataAlgorithms.NOTHING,
         UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION),
        (Algorithms.SUPPORT_VECTOR_MACHINES, UnbiasDataAlgorithms.REWEIGHING, UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.SUPPORT_VECTOR_MACHINES, UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER,
         UnbiasPostProcAlgorithms.NOTHING),
        # (Algorithms.SUPPORT_VECTOR_MACHINES, UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING,
        #  UnbiasPostProcAlgorithms.NOTHING),
        (Algorithms.SUPPORT_VECTOR_MACHINES, UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS,
         UnbiasPostProcAlgorithms.NOTHING),
        (UnbiasInProcAlgorithms.PREJUDICE_REMOVER, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING),
        (UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING),
        (UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION, UnbiasDataAlgorithms.NOTHING,
         UnbiasPostProcAlgorithms.NOTHING),
        (UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING),
        (UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING),
        (UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION, UnbiasDataAlgorithms.NOTHING, UnbiasPostProcAlgorithms.NOTHING)
    ]

    if args.dataset == 'ADULT_INCOME_SEX':
        datasets.append((Datasets.ADULT_INCOME, Preprocessors.SEX))
    elif args.dataset == 'ADULT_INCOME_FOREIGN':
        datasets.append((Datasets.GERMAN_CREDIT, Preprocessors.FOREIGN))
    elif args.dataset == 'GERMAN_CREDIT_AGE':
        datasets.append((Datasets.GERMAN_CREDIT, Preprocessors.AGE))
    elif args.dataset == 'LENDINGCLUB_INCOME':
        datasets.append((Datasets.LENDINGCLUB, Preprocessors.INCOME))

    for dataset, preprocessor in datasets:
        for preproc_alg, inproc_alg, postproc_alg in process_options:
            pipe.start(dataset, preprocessor, preproc_alg, inproc_alg, postproc_alg)


if __name__ == '__main__':
    execute_all()
