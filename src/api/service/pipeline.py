import main
from api.repo.pipeline import PipelineRepository


class PipelineService:
    pipeline_repository = PipelineRepository()

    def single_execution(self, request):
        main.execute_single(self.pipeline_repository.get_dataset(request['dataset']),
                            self.pipeline_repository.get_preprocessor(request['preprocessor']),
                            self.pipeline_repository.get_preproc_algorithm(request['preproc_algorithm']),
                            self.pipeline_repository.get_inproc_algorithm(request['inproc_algorithm']),
                            self.pipeline_repository.get_postproc_algorithm(request['postproc_algorithm']))

        return self.pipeline_repository.get_last_execution()

    def auto_execution(self, request):
        return main.mapek(self.pipeline_repository.get_dataset(request['dataset']))
