from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, UnbiasInProcAlgorithms, Algorithms, \
    UnbiasPostProcAlgorithms
from metrics.metrics import print_metrics
from pipeline.pipeline import Pipeline


def main():
    pipe = Pipeline()

    # y_test, y_pred, biased_explainer = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                               Algorithms.LOGISTIC_REGRESSION,
    #                                               UnbiasDataAlgorithms.NOTHING,
    #                                               UnbiasPostProcAlgorithms.NOTHING)

    rfy_test, rfy_pred, biased_explainer_rf = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                         Algorithms.RANDOM_FOREST,
                                                         UnbiasDataAlgorithms.NOTHING,
                                                         UnbiasPostProcAlgorithms.NOTHING)
    #
    # ry_test, ry_pred, unbiased_explainer_rw = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                      Algorithms.SUPPORT_VECTOR_MACHINES,
    #                                                      UnbiasDataAlgorithms.REWEIGHING,
    #                                                      UnbiasPostProcAlgorithms.NOTHING)
    #
    # ly_test, ly_pred, unbiased_explainer_lfr = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                       Algorithms.SUPPORT_VECTOR_MACHINES,
    #                                                       UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS,
    #                                                       UnbiasPostProcAlgorithms.NOTHING)
    #
    # diy_test, diy_pred, unbiased_explainer_dir = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                         Algorithms.SUPPORT_VECTOR_MACHINES,
    #                                                         UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER,
    #                                                         UnbiasPostProcAlgorithms.NOTHING)
    #
    # pry_test, pry_pred, unbiased_explainer_pr = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                        UnbiasInProcAlgorithms.PREJUDICE_REMOVER,
    #                                                        UnbiasDataAlgorithms.NOTHING,
    #                                                        UnbiasPostProcAlgorithms.NOTHING)
    #
    # ady_test, ady_pred, unbiased_explainer_ad = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                        UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING,
    #                                                        UnbiasDataAlgorithms.NOTHING,
    #                                                        UnbiasPostProcAlgorithms.NOTHING)

    # mfy_test, mfy_pred, unbiased_explainer_mf = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                        UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER,
    #                                                        UnbiasDataAlgorithms.NOTHING,
    #                                                        UnbiasPostProcAlgorithms.NOTHING)

    # rsy_test, rsy_pred, unbiased_explainer_rsf = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                         UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS,
    #                                                         UnbiasDataAlgorithms.NOTHING,
    #                                                         UnbiasPostProcAlgorithms.NOTHING)

    # egy_test, egy_pred, unbiased_explainer_egr = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                         UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION,
    #                                                         UnbiasDataAlgorithms.NOTHING,
    #                                                         UnbiasPostProcAlgorithms.NOTHING)

    gsy_test, gsy_pred, unbiased_explainer_gsr = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
                                                            UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION,
                                                            UnbiasDataAlgorithms.NOTHING,
                                                            UnbiasPostProcAlgorithms.NOTHING)

    # # atualizar pipe para ter conjunto de validação
    # rocy_test, rocy_pred, unbiased_explainer_roc = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                           UnbiasInProcAlgorithms.SUPPORT_VECTOR_MACHINES,
    #                                                           UnbiasDataAlgorithms.NOTHING,
    #                                                           UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION)
    #
    # eoy_test, eoy_pred, unbiased_explainer_eo = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                        UnbiasInProcAlgorithms.SUPPORT_VECTOR_MACHINES,
    #                                                        UnbiasDataAlgorithms.NOTHING,
    #                                                        UnbiasPostProcAlgorithms.EQUALIZED_ODDS)

    # ceoy_test, ceoy_pred, unbiased_explainer_ceo = pipe.start(Datasets.GERMAN_CREDIT, Preprocessors.AGE,
    #                                                           UnbiasInProcAlgorithms.LOGISTIC_REGRESSION,
    #                                                           UnbiasDataAlgorithms.NOTHING,
    #                                                           UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS)

    # biased_explainer.explain()
    # print_metrics(y_test, y_pred, biased_explainer, True)
    biased_explainer_rf.explain()
    print_metrics(rfy_test, rfy_pred, biased_explainer_rf, True)
    # unbiased_explainer_rw.explain()
    # print_metrics(ry_test, ry_pred, unbiased_explainer_rw, False)
    # unbiased_explainer_lfr.explain()
    # print_metrics(ly_test, ly_pred, unbiased_explainer_lfr, False)
    # unbiased_explainer_dir.explain()
    # print_metrics(diy_test, diy_pred, unbiased_explainer_dir, False)
    # unbiased_explainer_pr.explain()
    # print_metrics(pry_test, pry_pred, unbiased_explainer_pr, False)
    # unbiased_explainer_ad.explain()
    # print_metrics(ady_test, ady_pred, unbiased_explainer_ad, False)
    # unbiased_explainer_mf.explain()
    # print_metrics(mfy_test, mfy_pred, unbiased_explainer_mf, False)
    # unbiased_explainer_rsf.explain()
    # print_metrics(rsy_test, rsy_pred, unbiased_explainer_rsf, False)
    # unbiased_explainer_egr.explain()
    # print_metrics(egy_test, egy_pred, unbiased_explainer_egr, False)
    unbiased_explainer_gsr.explain()
    print_metrics(gsy_test, gsy_pred, unbiased_explainer_gsr, False)
    # unbiased_explainer_roc.explain()
    # print_metrics(rocy_test, rocy_pred, unbiased_explainer_roc, False)
    # unbiased_explainer_eo.explain()
    # print_metrics(eoy_test, eoy_pred, unbiased_explainer_eo, False)
    # unbiased_explainer_ceo.explain()
    # print_metrics(ceoy_test, ceoy_pred, unbiased_explainer_ceo, False)



if __name__ == '__main__':
    main()
