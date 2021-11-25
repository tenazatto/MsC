from mapek.steps.executor import MAPEKExecutor


class MLMAPEKPipelineExecutor(MAPEKExecutor):
    def execute(self, data):
        pipeline, plan = data

        print('Executando Pipeline')
        # pipeline.start(plan['dataset'], plan['preprocessor'],
        #                plan['unbias_data_algorithm'], plan['inproc_algorithm'], plan['unbias_postproc_algorithm'])
        print(plan)
        print('Pipeline executado')
