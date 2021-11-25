import json
import os
import pandas as pd

from mapek.steps.monitor import MAPEKMonitor


class MLMAPEKPipelineMonitor(MAPEKMonitor):
    def monitor(self):
        print('Coletando métricas')

        data = os.listdir('output/metrics')
        pd.set_option('display.max_columns', None)
        df_pipeline = pd.DataFrame(columns=['file_id', 'data_checksum', 'dataset', 'preprocessor', 'unbias_data_algorithm', 'inproc_algorithm',
                                            'unbias_postproc_algorithm'])
        df_metrics = pd.DataFrame(columns=['file_id', 'data_checksum', 'metric_id', 'metric_name', 'description', 'value'])

        for json_file in data:
            file_id = json_file.replace('.json', '')
            json_data = json.load(open('output/metrics/' + json_file, 'r'))

            df_pipeline.loc[df_pipeline.shape[0]] = [
                file_id,
                json_data['checksum'],
                json_data['pipeline_params']['dataset'],
                json_data['pipeline_params']['preprocessor'],
                json_data['pipeline_params']['unbias_data_algorithm'],
                json_data['pipeline_params']['algorithm'],
                json_data['pipeline_params']['unbias_postproc_algorithm']
            ]

            for metric in json_data['metrics_summary'].keys():
                metric_data = json_data['metrics_summary'][metric]

                df_metrics.loc[df_metrics.shape[0]] = [
                    file_id,
                    json_data['checksum'],
                    metric,
                    metric_data['name'],
                    metric_data['explanation'],
                    metric_data['value'][0] if type(metric_data['value']) == list else metric_data['value']
                ]

        print(df_pipeline)
        print(df_metrics)

        return df_pipeline, df_metrics
