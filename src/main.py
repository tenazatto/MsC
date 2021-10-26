from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, UnbiasInProcAlgorithms, Algorithms, \
    UnbiasPostProcAlgorithms

from pipeline.pipeline import Pipeline


def main():
    pipe = Pipeline()

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               Algorithms.LOGISTIC_REGRESSION,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               Algorithms.RANDOM_FOREST,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               Algorithms.SUPPORT_VECTOR_MACHINES,
               UnbiasDataAlgorithms.REWEIGHING,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               Algorithms.SUPPORT_VECTOR_MACHINES,
               UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               Algorithms.SUPPORT_VECTOR_MACHINES,
               UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               UnbiasInProcAlgorithms.PREJUDICE_REMOVER,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.NOTHING)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.NOTHING)

    # # atualizar pipe para ter conjunto de validação
    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               UnbiasInProcAlgorithms.SUPPORT_VECTOR_MACHINES,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               UnbiasInProcAlgorithms.SUPPORT_VECTOR_MACHINES,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.EQUALIZED_ODDS)

    pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
               UnbiasInProcAlgorithms.LOGISTIC_REGRESSION,
               UnbiasDataAlgorithms.NOTHING,
               UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS)


if __name__ == '__main__':
    main()
