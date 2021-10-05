from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, UnbiasInProcAlgorithms, Algorithms
from metrics.metrics import print_metrics
from pipeline.pipeline import Pipeline


def main():
    pipe = Pipeline()

    y_test, y_pred, biased_explainer = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                  Algorithms.LOGISTIC_REGRESSION,
                                                  UnbiasDataAlgorithms.NOTHING)

    ry_test, ry_pred, unbiased_explainer_rw = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                         Algorithms.LOGISTIC_REGRESSION,
                                                         UnbiasDataAlgorithms.REWEIGHING)

    diy_test, diy_pred, unbiased_explainer_dir = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                            Algorithms.LOGISTIC_REGRESSION,
                                                            UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER)

    pry_test, pry_pred, unbiased_explainer_pr = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                            UnbiasInProcAlgorithms.PREJUDICE_REMOVER,
                                                            UnbiasDataAlgorithms.NOTHING)

    biased_explainer.explain()
    print_metrics(y_test, y_pred, biased_explainer, True)
    unbiased_explainer_rw.explain()
    print_metrics(ry_test, ry_pred, unbiased_explainer_rw, False)
    unbiased_explainer_dir.explain()
    print_metrics(diy_test, diy_pred, unbiased_explainer_dir, False)
    unbiased_explainer_pr.explain()
    print_metrics(pry_test, pry_pred, unbiased_explainer_pr, False)


if __name__ == '__main__':
    main()
