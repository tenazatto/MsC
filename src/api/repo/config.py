import json


class ConfigRepository:
    folder = './config/mapek/'

    def get_file(self, file):
        return open(self.folder + file, 'r')

    def write_file(self, file, content):
        file = open(self.folder + file, 'w')
        file.write(json.dumps(content, indent=2))
        file.close()

    def get_analyzer_flags(self):
        return json.load(self.get_file('analyzer_flags.json'))

    def save_analyzer_flags(self, content):
        self.write_file('analyzer_flags.json', content)

    def get_metrics_weights(self):
        return json.load(self.get_file('metrics_weights.json'))

    def save_metrics_weights(self, content):
        self.write_file('metrics_weights.json', content)

    def get_planner_flags(self):
        return json.load(self.get_file('planner_flags.json'))

    def save_planner_flags(self, content):
        self.write_file('planner_flags.json', content)

    def get_score_threshold(self):
        return json.load(self.get_file('score_threshold.json'))

    def save_score_threshold(self, content):
        self.write_file('score_threshold.json', content)

    def get_valid_algorithms(self):
        return json.load(self.get_file('valid_algorithms.json'))

    def save_valid_algorithms(self, content):
        self.write_file('valid_algorithms.json', content)
