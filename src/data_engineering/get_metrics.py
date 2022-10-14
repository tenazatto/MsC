import json
import os
import statistics
from pprint import pprint

from tqdm import tqdm


def get_metrics():
    data = os.listdir('output/metrics')

    pipeline_metrics = group_metrics_by_param(data)
    pipeline_metrics = get_statistics(pipeline_metrics)

    pprint(pipeline_metrics, indent=4)
    json.dump(pipeline_metrics, open('metrics.json', 'w'), indent=4)


def group_metrics_by_param(data):
    pipeline_metrics = []

    for json_file in tqdm(data):
        json_data = json.load(open('output/metrics/' + json_file, 'r'))
        params = {
            'dataset': json_data['pipeline_params']['dataset'],
            'preprocessor': json_data['pipeline_params']['preprocessor'],
            'unbias_data_algorithm': json_data['pipeline_params']['unbias_data_algorithm'],
            'algorithm': json_data['pipeline_params']['algorithm'],
            'unbias_postproc_algorithm': json_data['pipeline_params']['unbias_postproc_algorithm']
        }
        performance_metrics = {
            'accuracy': json_data['metrics_summary']['accuracy']['value'],
            'precision': json_data['metrics_summary']['precision']['value'],
            'recall': json_data['metrics_summary']['recall']['value'],
            'f1_score': json_data['metrics_summary']['f1_score']['value'],
            'auc': json_data['metrics_summary']['auc']['value'],
        }
        fairness_metrics = {
            'statistical_parity_difference': json_data['metrics_summary']['statistical_parity_difference']['value'],
            'equal_opportunity_difference': json_data['metrics_summary']['equal_opportunity_difference']['value'],
            'average_odds_difference': json_data['metrics_summary']['average_odds_difference']['value'],
            'disparate_impact': json_data['metrics_summary']['disparate_impact']['value'],
            'theil_index': json_data['metrics_summary']['theil_index']['value']
        }

        if params in list(map(lambda metrics: metrics[0], pipeline_metrics)):
            for metrics in pipeline_metrics:
                if metrics[0] == params:
                    metrics[1].append(performance_metrics)
                    metrics[2].append(fairness_metrics)
                    break
        else:
            pipeline_metrics.append((params, [performance_metrics], [fairness_metrics]))

    return pipeline_metrics


def get_statistics(pipeline_metrics):
    pipeline_stats = []

    for metrics in pipeline_metrics:
        accuracy = get_min_max_mean('accuracy', metrics, 1)
        precision = get_min_max_mean('precision', metrics, 1)
        recall = get_min_max_mean('recall', metrics, 1)
        f1_score = get_min_max_mean('f1_score', metrics, 1)
        auc = get_min_max_mean('auc', metrics, 1)

        statistical_parity_difference = get_min_max_mean('statistical_parity_difference', metrics, 2)
        equal_opportunity_difference = get_min_max_mean('equal_opportunity_difference', metrics, 2)
        average_odds_difference = get_min_max_mean('average_odds_difference', metrics, 2)
        disparate_impact = get_min_max_mean('disparate_impact', metrics, 2)
        theil_index = get_min_max_mean('theil_index', metrics, 2)

        pipeline_stats.append({
            'params': metrics[0],
            'performance_metrics': {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score,
                'auc': auc
            },
            'fairness_metrics': {
                'statistical_parity_difference': statistical_parity_difference,
                'equal_opportunity_difference': equal_opportunity_difference,
                'average_odds_difference': average_odds_difference,
                'disparate_impact': disparate_impact,
                'theil_index': theil_index
            }
        })

    return pipeline_stats


def get_min_max_mean(metric_name, metrics, index):
    values = list(map(lambda m: m[metric_name], metrics[index]))
    return {'min': min(values), 'max': max(values), 'mean': statistics.mean(values)}
