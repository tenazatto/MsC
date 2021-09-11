import pandas as pd


class FairnessPreprocessor:
    dataset_path = ''
    privileged_group = []
    unprivileged_group = []

    label_names = []
    protected_attribute_names = []

    def load_dataset(self):
        return pd.read_csv(self.dataset_path)

    def dataset_preprocess(self):
        pass
