from pipeline.pipe_filter.pipe import BasePipe

import pandas as pd


class Dataset(BasePipe):
    dataset_path = ''

    def load_dataset(self):
        self.value = pd.read_csv(self.dataset_path)

    def __init__(self):
        self.load_dataset()


class GermanDataset(Dataset):
    dataset_path = 'datasets/german_credit_data.csv'

    def __init__(self):
        super().__init__()

class AdultDataset(Dataset):
    dataset_path = 'datasets/adult.csv'

    def __init__(self):
        super().__init__()
