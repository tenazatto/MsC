class PipeFilter:
    pass

class BasePipe(PipeFilter):
    value = None

    def merge(self, other):
        if not isinstance(other, BasePipe):
            raise Exception("Um Pipe só pode se unir com um Pipe")

        new_pipe = self
        new_pipe.value.update(other.value)

        return new_pipe

    def partial_pipe(self, attributes):
        new_pipe = BasePipe()
        new_pipe.value = {}

        for attribute in attributes:
            if attribute in self.value.keys():
                new_pipe.value[attribute] = self.value[attribute]

        return new_pipe

    def __ge__(self, other: PipeFilter):
        if not isinstance(other, BaseFilter):
            raise Exception("Um Pipe só pode se encadear com um Filtro")

        print('teste de encadear pipe com ' + str(other))

        other.input = self.value

        return other

class BaseFilter(PipeFilter):
    input = None
    output = None

    def execute(self):
        self.output = self.input

    def __eq__(self, other: PipeFilter):
        if not isinstance(other, BasePipe):
            raise Exception("Um Filtro só pode se encadear com um Pipe")

        self.execute()

        other.value = self.output

        return other