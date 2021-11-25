from mapek.steps.planner import MAPEKPlanner


class MLMAPEKPipelinePlanner(MAPEKPlanner):
    def plan(self, data):
        print('Efetuando estratégia de planejamento')
        result = data.iloc[0]

        return {
            'dataset': result['dataset'],
            'preprocessor': result['preprocessor'],
            'unbias_data_algorithm': result['unbias_data_algorithm'],
            'inproc_algorithm': result['inproc_algorithm'],
            'unbias_postproc_algorithm': result['unbias_postproc_algorithm']
        }
