import numpy as np
from tensorflow.python.summary.summary_iterator import summary_iterator

import matplotlib as mpl
import matplotlib.pyplot as plt

def update_iteration(last_iteration, dataset):
    if(dataset == "products"):
        batches = [1000, 250]
    else:
        batches = [500, 100]

    iterations = last_iteration
    if (iterations < 5000):
        iterations += batches[0]
    else:
        iterations += batches[1]

    return iterations

def get_results(path, dataset):
    results = []

    iterations = 0
    for event in summary_iterator(path):
        dict_result = {}

        if(len(event.summary.value) == 0):
            print("NOK")
        else:
            iterations = update_iteration(iterations, dataset)
            dict_result["iteration"] = iterations
            for value in event.summary.value:
                if value.HasField('simple_value'):
                    dict_result[value.tag.replace(' ', '_')] = value.simple_value

            results.append(dict_result)

    print(results)

    return results

def get_logs(path, dataset, loss):
    dict_logs = {}
    dict_logs["loss"] = loss
    dict_logs["dataset"] = dataset
    dict_logs["path"] = path
    dict_logs["results"] = get_results(path, dataset)

    return dict_logs

# f1_scores = list(map(lambda result: result["test_f1"], summary[0]["results"]))
# nmi = list(map(lambda result: result["test_nmi"], summary[0]["results"]))
# recall = list(map(lambda result: result["Recall@1_test"], summary[0]["results"]))
# loss = list(map(lambda result: result["Jm"], summary[0]["results"]))


def plot_tensorflow_log_loss(summary):
    for exp in summary:
        iterations = list(map(lambda result: result["iteration"], exp["results"]))
        loss = list(map(lambda result: result["Jm"], exp["results"]))
        plt.plot(iterations, loss, label=(exp["loss"] + " - " + exp["dataset"]))

    plt.xlabel("Steps")
    plt.ylabel("Value")
    plt.title("Metric Learning Loss Functions")
    plt.legend(loc='lower left', frameon=True)

def plot_tensorflow_log_f1(summary):
    for exp in summary:
        iterations = list(map(lambda result: result["iteration"], exp["results"]))
        f1_scores = list(map(lambda result: result["test_f1"], exp["results"]))
        plt.plot(iterations, f1_scores, label=(exp["loss"] + " - " + exp["dataset"]))

    plt.xlabel("Steps")
    plt.ylabel("Value")
    plt.title("Metric Learning F1-Score")
    plt.legend(loc='lower left', frameon=True)

def plot_tensorflow_log_recall(summary):
    for exp in summary:
        iterations = list(map(lambda result: result["iteration"], exp["results"]))
        recall = list(map(lambda result: result["Recall@1_test"], exp["results"]))
        plt.plot(iterations, recall, label=(exp["loss"] + " - " + exp["dataset"]))

    plt.xlabel("Steps")
    plt.ylabel("Value")
    plt.title("Metric Learning Recall")
    plt.legend(loc='lower left', frameon=True)

def plot_tensorflow_log_nmi(summary):
    for exp in summary:
        iterations = list(map(lambda result: result["iteration"], exp["results"]))
        nmi = list(map(lambda result: result["test_nmi"], exp["results"]))
        plt.plot(iterations, nmi, label=(exp["loss"] + " - " + exp["dataset"]))

    plt.xlabel("Steps")
    plt.ylabel("Value")
    plt.title("Metric Learning NMI")
    plt.legend(loc='lower left', frameon=True)

if __name__ == '__main__':
    logs = [
        ("/home/thales.nazatto/Pós/MsC/MetricLearning/tensorboard_log/cars196/NpairLoss/05-20-20-05/events.out.tfevents.1590016614.PE03GM77", "cars196", "NpairLoss"),
        ("/home/thales.nazatto/Pós/MsC/MetricLearning/tensorboard_log/cars196/Triplet/05-20-23-43/events.out.tfevents.1590029670.PE03GM77", "cars196", "Triplet"),
        ("/home/thales.nazatto/Pós/MsC/MetricLearning/tensorboard_log/cub200_2011/NpairLoss/05-21-22-48/events.out.tfevents.1590112745.PE03GM77", "cub200_2011", "NpairLoss"),
        ("/home/thales.nazatto/Pós/MsC/MetricLearning/tensorboard_log/cub200_2011/Triplet/05-21-19-51/events.out.tfevents.1590102056.PE03GM77", "cub200_2011", "Triplet"),
        ("/home/thales.nazatto/Pós/MsC/MetricLearning/tensorboard_log/products/NpairLoss/05-22-18-04/events.out.tfevents.1590183093.PE03GM77", "products", "NpairLoss"),
        ("/home/thales.nazatto/Pós/MsC/MetricLearning/tensorboard_log/products/Triplet/05-22-01-50/events.out.tfevents.1590124613.PE03GM77", "products", "Triplet")
    ]
    summary = []
    for log in logs:
        summary.append(get_logs(log[0], log[1], log[2]))

    print(summary)
    #plot_tensorflow_log_loss(summary)
    #plot_tensorflow_log_f1(summary)
    plot_tensorflow_log_recall(summary)
    #plot_tensorflow_log_nmi(summary)
    plt.show()