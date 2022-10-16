from src.mapek.steps.executor import MAPEKExecutor


class MLMAPEKPipelineExecutor(MAPEKExecutor):
    def execute(self, data):
        pipeline, plan = data

        print('Executando Pipeline')
        plan_executed = plan.iloc[0]
        pipeline.start(plan_executed['dataset'], plan_executed['preprocessor'],
                       plan_executed['inproc_algorithm'],
                       plan_executed['unbias_data_algorithm'],
                       plan_executed['unbias_postproc_algorithm'],
                       save_metadata=False)
        print(plan_executed)
        print('Pipeline executado')
