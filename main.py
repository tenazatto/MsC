from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, UnbiasInProcAlgorithms, Algorithms
from metrics.metrics import print_metrics
from pipeline.pipeline import Pipeline


def main():
    pipe = Pipeline()

    y_test, y_pred, biased_explainer = pipe.start(Datasets.ADULT_INCOME, Preprocessors.SEX,
                                                  Algorithms.LOGISTIC_REGRESSION,
                                                  UnbiasDataAlgorithms.NOTHING)

    ry_test, ry_pred, unbiased_explainer_rw = pipe.start(Datasets.ADULT_INCOME, Preprocessors.SEX,
                                                         Algorithms.LOGISTIC_REGRESSION,
                                                         UnbiasDataAlgorithms.REWEIGHING)

    diy_test, diy_pred, unbiased_explainer_dir = pipe.start(Datasets.ADULT_INCOME, Preprocessors.SEX,
                                                            Algorithms.LOGISTIC_REGRESSION,
                                                            UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER)

    pry_test, pry_pred, unbiased_explainer_pr = pipe.start(Datasets.ADULT_INCOME, Preprocessors.SEX,
                                                            UnbiasInProcAlgorithms.PREJUDICE_REMOVER,
                                                            UnbiasDataAlgorithms.NOTHING)

    print_metrics(y_test, y_pred, biased_explainer, True)
    print_metrics(ry_test, ry_pred, unbiased_explainer_rw, False)
    print_metrics(diy_test, diy_pred, unbiased_explainer_dir, False)
    print_metrics(pry_test, pry_pred, unbiased_explainer_pr, False)

if __name__ == '__main__':
    main()
