from sklearn.model_selection import train_test_split

from src.pipeline.pipe_filter.pipe import BaseFilter


class TrainTestSplit(BaseFilter):
    test_size = 0.2

    def __init__(self, test_size=0.2):
        self.test_size = test_size

    def execute(self):
        df_x = self.input['df_x']
        df_y = self.input['df_y']

        x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=self.test_size, random_state=42)

        self.output = {
            'x_train': x_train,
            'x_test': x_test,
            'y_train': y_train,
            'y_test': y_test,
            'checksum': self.input['checksum']
        }
