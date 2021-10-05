import pandas as pd
from aif360.algorithms.preprocessing import Reweighing, OptimPreproc, DisparateImpactRemover
from aif360.algorithms.preprocessing.optim_preproc_helpers.opt_tools import OptTools
from aif360.datasets import BinaryLabelDataset


def prejudice_remover_preprocess(x_train, x_test, y_train, y_test, preprocessor):
    df_aif_tr = BinaryLabelDataset(df=pd.concat((x_train, y_train), axis=1), label_names=preprocessor.label_names,
                                   protected_attribute_names=preprocessor.protected_attribute_names)
    print(df_aif_tr)

    df_aif_te = BinaryLabelDataset(df=pd.concat((x_test, y_test), axis=1), label_names=preprocessor.label_names,
                                   protected_attribute_names=preprocessor.protected_attribute_names)
    print(df_aif_te)

    return df_aif_tr, df_aif_te


def reweighing_preprocess(x_train, y_train, preprocessor):
    df_aif = BinaryLabelDataset(df=pd.concat((x_train, y_train), axis=1), label_names=preprocessor.label_names,
                                protected_attribute_names=preprocessor.protected_attribute_names)
    print(df_aif)

    RW = Reweighing(preprocessor.unprivileged_group, preprocessor.privileged_group)
    df_aif_rw = RW.fit_transform(df_aif)

    return df_aif_rw


def disparate_impact_preprocess(x_train, x_test, y_train, y_test, preprocessor):
    df_aif_tr = BinaryLabelDataset(df=pd.concat((x_train, y_train), axis=1), label_names=preprocessor.label_names,
                                   protected_attribute_names=preprocessor.protected_attribute_names)
    print(df_aif_tr)

    df_aif_te = BinaryLabelDataset(df=pd.concat((x_test, y_test), axis=1), label_names=preprocessor.label_names,
                                   protected_attribute_names=preprocessor.protected_attribute_names)
    print(df_aif_te)

    di = DisparateImpactRemover(repair_level=1)
    df_aif_di_tr = di.fit_transform(df_aif_tr)
    df_aif_di_te = di.fit_transform(df_aif_te)

    x_di_train = df_aif_di_tr.features
    x_di_test = df_aif_di_te.features
    y_di_train = df_aif_di_tr.labels.ravel()

    return x_di_train, x_di_test, y_di_train, df_aif_te


def optim_preprocess(x_train, y_train, preprocessor):
    df_aif = BinaryLabelDataset(df=pd.concat((x_train, y_train), axis=1), label_names=preprocessor.label_names,
                                protected_attribute_names=preprocessor.protected_attribute_names)
    print(df_aif)

    OP = OptimPreproc(OptTools, preprocessor.optim_options, preprocessor.unprivileged_group, preprocessor.privileged_group)
    df_aif_op = OP.fit_transform(df_aif)
    df_aif_op = df_aif.align_datasets(df_aif_op)

    return df_aif_op
