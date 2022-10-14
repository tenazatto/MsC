from src.pipeline.pipe_filter.pipe import BaseFilter, BasePipe


class FairnessPipe(BasePipe):
    privileged_group = []
    unprivileged_group = []

    label_names = []
    protected_attribute_names = []

    optim_options = {}

    def __init__(self):
        self.value = {
            'privileged_group': self.privileged_group,
            'unprivileged_group': self.unprivileged_group,
            'label_names': self.label_names,
            'protected_attribute_names': self.protected_attribute_names,
            'optim_options': self.optim_options
        }


class FairnessPreprocessor(BaseFilter):
    def dataset_preprocess(self, df):
        pass

    def execute(self):
        df_x, df_y = self.dataset_preprocess(self.input['data'])

        self.output = {
            'df_x': df_x,
            'df_y': df_y,
            'checksum': self.input['checksum']
        }
