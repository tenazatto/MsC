import json
import os
import pandas as pd
from tqdm import tqdm

from mapek.steps.monitor import MAPEKMonitor


class MLMAPEKPipelineMonitor(MAPEKMonitor):
    def monitor(self):
        print('Coletando métricas')

        data = os.listdir('output/metrics')
        lst_pipeline = []
        lst_metrics = []
        pd.set_option('display.max_columns', None)

        for json_file in tqdm(data):
            file_id = json_file.replace('.json', '')
            json_data = json.load(open('output/metrics/' + json_file, 'r'))

            lst_pipeline.append({
                'file_id': file_id,
                'data_checksum': json_data['checksum'],
                'date_start': json_data['date_start'],
                'date_end': json_data['date_end'],
                'execution_time_ms': json_data['execution_time_ms'],
                'dataset': json_data['pipeline_params']['dataset'],
                'preprocessor': json_data['pipeline_params']['preprocessor'],
                'unbias_data_algorithm': json_data['pipeline_params']['unbias_data_algorithm'],
                'inproc_algorithm': json_data['pipeline_params']['algorithm'],
                'unbias_postproc_algorithm': json_data['pipeline_params']['unbias_postproc_algorithm']
            })

            for metric in json_data['metrics_summary'].keys():
                metric_data = json_data['metrics_summary'][metric]

                lst_metrics.append({
                    'file_id': file_id,
                    'data_checksum': json_data['checksum'],
                    'metric_id': metric,
                    'metric_name': metric_data['name'],
                    'description': metric_data['explanation'],
                    'value': metric_data['value'][0] if type(metric_data['value']) == list else metric_data['value']
                })

        df_pipeline = pd.DataFrame(lst_pipeline)
        df_metrics = pd.DataFrame(lst_metrics)

        return df_pipeline, df_metrics
