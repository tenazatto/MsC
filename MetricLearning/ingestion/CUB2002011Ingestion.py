import os
import random
import subprocess

import numpy as np

from datasetingestion import DatasetIngestion


class CUB2002011Ingestion(DatasetIngestion):
    def decompress(self, images_path, image_filepath):
        if not os.path.exists(images_path):
            subprocess.call(["tar", "zxvf", image_filepath.replace("\\", "/"),
                             "-C", images_path.replace("\\", "/"),
                             "--force-local"])

    def getClasses(self):
        id_img_pairs = np.loadtxt("./datasets/CUB/images.txt", np.str)
        assert np.array_equal(
            [int(i) for i in id_img_pairs[:, 0].tolist()], range(1, 11789))
        id_label_pairs = np.loadtxt("./datasets/CUB/image_class_labels.txt", np.str)
        assert np.array_equal(
            [int(i) for i in id_label_pairs[:, 0].tolist()], range(1, 11789))
        id_name_pairs = np.loadtxt("./datasets/CUB/classes.txt", np.str)
        num_classes = 200
        assert np.array_equal([int(i) for i in id_name_pairs[:, 0].tolist()], range(1, num_classes + 1))

        images = id_img_pairs[:, 1].tolist()
        class_labels = [int(i) for i in id_label_pairs[:, 1].tolist()]
        class_names = [self.birdName(name) for name in id_name_pairs[:, 1].tolist()]

        assert np.array_equal(np.unique(class_labels), range(1, num_classes + 1))

        return images, class_labels, class_names

    def getTestSamples(self, images, class_labels, class_names, num_classes, images_path):
        testClasses = sorted(random.sample(list(np.unique(class_labels)), k=num_classes))
        testIndexes = [index for index, value in enumerate(class_labels) if value in testClasses]
        testImages = [os.path.join(images_path, value) for index, value in enumerate(images) if index in testIndexes]
        testLabels = [value for index, value in enumerate(class_labels) if index in testIndexes]
        testNames = [class_names[label - 1] for label in testLabels]

        return testImages, testLabels, testNames

    def birdName(self, name):
        names = name.split('.')[1].split('_')

        final_name = ""
        for i in range(0, len(names)):
            if i == 0:
                final_name += names[i]
            elif names[i].islower():
                final_name += "-" + names[i]
            else:
                final_name += " " + names[i]

        return final_name
