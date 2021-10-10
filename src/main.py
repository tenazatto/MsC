from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, UnbiasInProcAlgorithms, Algorithms, \
    UnbiasPostProcAlgorithms
from metrics.metrics import print_metrics
from pipeline.pipeline import Pipeline


def main():
    pipe = Pipeline()

    y_test, y_pred, biased_explainer = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                  Algorithms.LOGISTIC_REGRESSION,
                                                  UnbiasDataAlgorithms.NOTHING,
                                                  UnbiasPostProcAlgorithms.NOTHING)

    ry_test, ry_pred, unbiased_explainer_rw = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                         Algorithms.LOGISTIC_REGRESSION,
                                                         UnbiasDataAlgorithms.REWEIGHING,
                                                         UnbiasPostProcAlgorithms.NOTHING)

    ly_test, ly_pred, unbiased_explainer_lfr = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                          Algorithms.LOGISTIC_REGRESSION,
                                                          UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS,
                                                          UnbiasPostProcAlgorithms.NOTHING)

    diy_test, diy_pred, unbiased_explainer_dir = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                            Algorithms.LOGISTIC_REGRESSION,
                                                            UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER,
                                                            UnbiasPostProcAlgorithms.NOTHING)

    pry_test, pry_pred, unbiased_explainer_pr = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                           UnbiasInProcAlgorithms.PREJUDICE_REMOVER,
                                                           UnbiasDataAlgorithms.NOTHING,
                                                           UnbiasPostProcAlgorithms.NOTHING)

    ady_test, ady_pred, unbiased_explainer_ad = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                           UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING,
                                                           UnbiasDataAlgorithms.NOTHING,
                                                           UnbiasPostProcAlgorithms.NOTHING)

    # atualizar pipe para ter conjunto de validação
    rocy_test, rocy_pred, unbiased_explainer_roc = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                              UnbiasInProcAlgorithms.LOGISTIC_REGRESSION,
                                                              UnbiasDataAlgorithms.NOTHING,
                                                              UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION)

    eoy_test, eoy_pred, unbiased_explainer_eo = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                           UnbiasInProcAlgorithms.LOGISTIC_REGRESSION,
                                                           UnbiasDataAlgorithms.NOTHING,
                                                           UnbiasPostProcAlgorithms.EQUALIZED_ODDS)

    ceoy_test, ceoy_pred, unbiased_explainer_ceo = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                              UnbiasInProcAlgorithms.LOGISTIC_REGRESSION,
                                                              UnbiasDataAlgorithms.NOTHING,
                                                              UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS)

    biased_explainer.explain()
    print_metrics(y_test, y_pred, biased_explainer, True)
    unbiased_explainer_rw.explain()
    print_metrics(ry_test, ry_pred, unbiased_explainer_rw, False)
    unbiased_explainer_lfr.explain()
    print_metrics(ly_test, ly_pred, unbiased_explainer_lfr, False)
    unbiased_explainer_dir.explain()
    print_metrics(diy_test, diy_pred, unbiased_explainer_dir, False)
    unbiased_explainer_pr.explain()
    print_metrics(pry_test, pry_pred, unbiased_explainer_pr, False)
    unbiased_explainer_ad.explain()
    print_metrics(ady_test, ady_pred, unbiased_explainer_ad, False)
    unbiased_explainer_roc.explain()
    print_metrics(rocy_test, rocy_pred, unbiased_explainer_roc, False)
    unbiased_explainer_eo.explain()
    print_metrics(eoy_test, eoy_pred, unbiased_explainer_eo, False)
    unbiased_explainer_ceo.explain()
    print_metrics(ceoy_test, ceoy_pred, unbiased_explainer_ceo, False)



if __name__ == '__main__':
    main()
