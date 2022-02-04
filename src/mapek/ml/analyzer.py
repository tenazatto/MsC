import json

import pandas as pd

from mapek.steps.analyzer import MAPEKAnalyzer


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
        df_score = pd.DataFrame(columns=['file_id', 'score'])
        for file_id in df_metrics_group['file_id'].unique():
            df_file = df_metrics_group[df_metrics_group['file_id'] == file_id]
            score = 0
            for metric in metrics_weights.keys():
                metric_final = self.normalize_metric(df_file[df_file['metric_id'] == metric].iloc[0]['value'],
                                                     metrics_weights[metric]['normalize'])

                score += round(1000 * metrics_weights[metric]['weight'] * metric_final)

            df_score.loc[df_score.shape[0]] = [
                file_id,
                score
            ]

        return df_score

    def apply_group_score(self, scores_and_weights):
        df_score = pd.DataFrame(columns=['file_id', 'score'])
        standard = scores_and_weights[0]
        fairness = scores_and_weights[1]
        for file_id in standard[0]['file_id'].unique():
            score = standard[0][standard[0]['file_id'] == file_id]['score'] * standard[1] + \
                    fairness[0][fairness[0]['file_id'] == file_id]['score'] * fairness[1]
            score = round(score.iloc[0])
            df_score.loc[df_score.shape[0]] = [
                file_id,
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
        return 1 / metric if metric > 1 else metric

    def normalize_diff(self, metric):
        return abs(1-metric)


class MLMAPEKPipelineAnalyzer(MAPEKAnalyzer):
    def do_analysis(self, data):
        print('Efetuando análise de métricas ' + self.__class__.__name__)

        group_data = data[0].groupby(['data_checksum', 'dataset', 'preprocessor',
                                     'unbias_data_algorithm',
                                     'inproc_algorithm',
                                     'unbias_postproc_algorithm'])
        date_data = group_data.max()['date_end']
        mean_data = group_data.mean().round().astype('int32')

        group_data = mean_data.merge(date_data, on=['data_checksum', 'dataset', 'preprocessor',
                                                   'unbias_data_algorithm',
                                                   'inproc_algorithm',
                                                   'unbias_postproc_algorithm'])
        group_data = group_data.rename(columns={"date_end": "last_date_end"})

        return group_data.reset_index().sort_values('score', ascending=False)
