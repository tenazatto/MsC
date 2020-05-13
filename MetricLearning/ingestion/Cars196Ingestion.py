import os
import random
import subprocess

import numpy as np
from scipy.io import loadmat

from datasetingestion import DatasetIngestion


class Cars196Ingestion(DatasetIngestion):
    def decompress(self, images_path, image_filepath):
        if not os.path.exists(images_path):
            subprocess.call(["tar", "zxvf", image_filepath.replace("\\", "/"),
                             "-C", images_path.replace("\\", "/"),
                             "--force-local"])

    def getClasses(self):
        cars196Lbl = loadmat("./datasets/cars196/cars_annos.mat")

        images = self.getClassAttrs(cars196Lbl, "annotations", 0, None)
        class_labels = self.getClassAttrs(cars196Lbl, "annotations", 5, int)
        class_names = self.getClassAttrs(cars196Lbl, "class_names", 0, None)

        # Ver nomes
        return images, class_labels, class_names

    def getTestSamples(self, images, class_labels, class_names, num_classes, images_path):
        testClasses = sorted(random.sample(list(np.unique(class_labels)), k=num_classes))
        testIndexes = [index for index, value in enumerate(class_labels) if value in testClasses]
        testImages = [value[0].replace('car_ims', images_path) for index, value in enumerate(images) if
                      index in testIndexes]
        testLabels = [value for index, value in enumerate(class_labels) if index in testIndexes]
        testNames = [class_names[label - 1] for label in testLabels]

        return testImages, testLabels, testNames

    def getClassAttrs(self, dataset, index, idxAttr, type):
        attrs = dataset[index].ravel()
        attrs = sorted(attrs, key=lambda a: str(a[0][0]))
        class_attrs = []
        for attr in attrs:
            class_attr = attr[idxAttr] if type is None else type(attr[idxAttr])
            class_attrs.append(class_attr)

        return class_attrs
