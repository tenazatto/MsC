import json

import pandas as pd

from src.mapek.steps.analyzer import MAPEKAnalyzer


class MLMAPEKExecutionAnalyzer(MAPEKAnalyzer):
    def do_analysis(self, data):
        print('Efetuando análise de métricas ' + self.__class__.__name__)

        df_pipeline, df_metrics = data
        df_fairness, df_standard = self.get_weights()

        df_fairness_metrics, df_standard_metrics = self.get_metrics_dfs(df_fairness, df_metrics, df_standard)

        df_standard_score = self.apply_metrics_score(df_standard_metrics, df_standard['metrics'])
        df_fairness_score = self.apply_metrics_score(df_fairness_metrics, df_fairness['metrics'])

        df_score = self.apply_group_score([(df_standard_score, df_standard["weight"]),
                                           (df_fairness_score, df_fairness["weight"])])

        df_pipeline_score = df_pipeline.merge(df_score, on='file_id').sort_values('score', ascending=False)

        return df_pipeline_score

    def get_weights(self):
        weights = json.load(open('config/mapek/metrics_weights.json', 'r'))
        df_weights = pd.DataFrame.from_dict(weights["metrics_groups"])

        df_standard = df_weights[df_weights["group_name"] == "standard"].iloc[0]
        df_fairness = df_weights[df_weights["group_name"] == "fairness"].iloc[0]

        return df_fairness, df_standard

    def get_metrics_dfs(self, df_fairness, df_metrics, df_standard):
        df_standard_metrics = df_metrics[df_metrics["metric_id"].isin(df_standard['metrics'].keys())]
        df_fairness_metrics = df_metrics[df_metrics["metric_id"].isin(df_fairness['metrics'].keys())]

        invalid_ids = pd.concat([df_standard_metrics[df_standard_metrics['value'].isnull()]['file_id'],
                                 df_fairness_metrics[df_fairness_metrics['value'].isnull()]['file_id']]).unique()

        df_standard_metrics = df_standard_metrics[~df_standard_metrics['file_id'].isin(invalid_ids)]
        df_fairness_metrics = df_fairness_metrics[~df_fairness_metrics['file_id'].isin(invalid_ids)]

        return df_fairness_metrics, df_standard_metrics

    def apply_metrics_score(self, df_metrics_group, metrics_weights):
        max_score = 1000
        df_score = pd.DataFrame(columns=['file_id', 'score'])
        for file_id in df_metrics_group['file_id'].unique():
            df_file = df_metrics_group[df_metrics_group['file_id'] == file_id]
            score = 0
            for metric in metrics_weights.keys():
                metric_final = self.normalize_metric(df_file[df_file['metric_id'] == metric].iloc[0]['value'],
                                                     metrics_weights[metric]['normalize'])

                score += round(max_score * metrics_weights[metric]['weight'] * metric_final)

            df_score.loc[df_score.shape[0]] = [
                file_id,
                score
            ]

        return df_score

    def apply_group_score(self, scores_and_weights):
        df_score = pd.DataFrame(columns=['file_id', 'standard_score', 'fairness_score', 'score'])
        standard = scores_and_weights[0]
        fairness = scores_and_weights[1]
        for file_id in standard[0]['file_id'].unique():
            standard_score = standard[0][standard[0]['file_id'] == file_id]['score']
            fairness_score = fairness[0][fairness[0]['file_id'] == file_id]['score']
            score = standard_score * standard[1] + fairness_score * fairness[1]
            score = round(score.iloc[0])
            df_score.loc[df_score.shape[0]] = [
                file_id,
                standard_score.iloc[0],
                fairness_score.iloc[0],
                score
            ]

        return df_score

    def normalize_metric(self, metric, normalize):
        if normalize == 'ratio':
            return self.normalize_ratio(metric)
        elif normalize == 'diff':
            return self.normalize_diff(metric)

        return metric

    def normalize_ratio(self, metric):
        return 1-abs(1/metric-1) if metric > 1 else 1-abs(metric-1)

    def normalize_diff(self, metric):
        return 1-abs(metric) if -1 < metric < 1 else 0


class MLMAPEKPipelineAnalyzer(MAPEKAnalyzer):
    def do_analysis(self, data):
        print('Efetuando análise de métricas ' + self.__class__.__name__)

        group_data = data[0].groupby(['data_checksum', 'dataset', 'preprocessor',
                                     'unbias_data_algorithm',
                                     'inproc_algorithm',
                                     'unbias_postproc_algorithm'])
        date_data = group_data.max()['date_end']
        mean_data_score = group_data['standard_score', 'fairness_score', 'score']\
            .mean().round().astype('int32')
        mean_data_time = group_data['execution_time_ms']\
            .mean().round().astype('int32')

        group_data = mean_data_score \
            .merge(mean_data_time, on=['data_checksum', 'dataset', 'preprocessor',
                                  'unbias_data_algorithm',
                                  'inproc_algorithm',
                                  'unbias_postproc_algorithm'])\
            .merge(date_data, on=['data_checksum', 'dataset', 'preprocessor',
                                                   'unbias_data_algorithm',
                                                   'inproc_algorithm',
                                                   'unbias_postproc_algorithm'])
        group_data = group_data.rename(columns={"date_end": "last_date_end"})

        return group_data.reset_index().sort_values('score', ascending=False)
