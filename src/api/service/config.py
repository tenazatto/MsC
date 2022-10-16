from src.api.repo.config import ConfigRepository


class ConfigService:
    config_repository = ConfigRepository()

    def get_metrics_configuration(self):
        return self.config_repository.get_metrics_weights()

    def save_metrics_configuration(self, content):
        self.config_repository.save_metrics_weights(content)

    def get_score_configuration(self):
        return self.config_repository.get_score_threshold()

    def save_score_configuration(self, content):
        self.config_repository.save_score_threshold(content)

    def get_planner_configuration(self):
        return self.config_repository.get_planner_flags()

    def save_planner_configuration(self, content):
        self.config_repository.save_planner_flags(content)

    def get_analyzer_configuration(self):
        return self.config_repository.get_analyzer_flags()

    def save_analyzer_configuration(self, content):
        self.config_repository.save_analyzer_flags(content)

    def get_valid_algorithms_configuration(self):
        return self.config_repository.get_valid_algorithms()

    def save_valid_algorithms_configuration(self, content):
        self.config_repository.save_valid_algorithms(content)
