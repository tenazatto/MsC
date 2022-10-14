from sklearn.model_selection import train_test_split

from src.pipeline.pipe_filter.pipe import BaseFilter


class TrainValidTestSplit(BaseFilter):
    test_size = 0.15
    valid_size = 0.15

    def __init__(self, test_size=0.15, valid_size=0.15):
        self.test_size = test_size
        self.valid_size = valid_size

    def execute(self):
        df_x = self.input['df_x']
        df_y = self.input['df_y']

        x_trval, x_test, y_trval, y_test = train_test_split(df_x, df_y, test_size=self.test_size, random_state=42)

        valid_split_size = self.valid_size / (1 - self.test_size)

        x_train, x_val, y_train, y_val = train_test_split(x_trval, y_trval, test_size=valid_split_size, random_state=42)

        self.output = {
            'x_train': x_train,
            'x_val': x_val,
            'x_test': x_test,
            'y_train': y_train,
            'y_val': y_val,
            'y_test': y_test,
            'checksum': self.input['checksum']
        }
