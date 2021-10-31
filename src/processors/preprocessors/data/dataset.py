import hashlib

from pipeline.pipe_filter.pipe import BasePipe

import pandas as pd


class Dataset(BasePipe):
    dataset_path = ''

    def load_dataset(self):
        df = pd.read_csv(self.dataset_path)
        checksum = hashlib.sha512(pd.util.hash_pandas_object(df).values).hexdigest()

        self.value = {
            'data': df,
            'checksum': checksum
        }

    def __init__(self):
        self.load_dataset()


class GermanDataset(Dataset):
    dataset_path = 'src/datasets/german_credit_data.csv'

    def __init__(self):
        super().__init__()

class AdultDataset(Dataset):
    dataset_path = 'src/datasets/adult.csv'

    def __init__(self):
        super().__init__()
