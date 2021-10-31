class PipeFilter:
    pass


class BasePipe(PipeFilter):
    value = None

    def merge(self, other):
        if not isinstance(other, BasePipe):
            raise Exception("Um Pipe só pode se unir a um Pipe")

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

    def to_filter(self, filter):
        if not isinstance(filter, BaseFilter):
            raise Exception("Um Pipe só pode se encadear com um Filtro")

        print('Encadeando pipe com ' + str(filter))

        filter.input = self.value

        return filter

    def __add__(self, other: PipeFilter):
        return self.merge(other)

    def __getitem__(self, item):
        if type(item) == dict:
            item = item.keys()
        elif type(item) != list and type(item) != tuple:
            item = [item]

        return self.partial_pipe(item)

    def __ge__(self, other: PipeFilter):
        return self.to_filter(other)


class BaseFilter(PipeFilter):
    input = None
    output = None

    def execute(self):
        self.output = self.input

    def to_pipe(self, pipe: PipeFilter):
        if not isinstance(pipe, BasePipe):
            raise Exception("Um Filtro só pode se encadear com um Pipe")

        self.execute()

        pipe.value = self.output

        return pipe

    def __eq__(self, other: PipeFilter):
        return self.to_pipe(other)
