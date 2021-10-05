from pipeline.pipe_filter.pipe import BaseFilter, BasePipe


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
    def dataset_preprocess(self):
        pass

    def execute(self):
        x_train, x_test, y_train, y_test = self.dataset_preprocess()
        self.output = {
            'x_train': x_train,
            'x_test': x_test,
            'y_train': y_train,
            'y_test': y_test
        }
