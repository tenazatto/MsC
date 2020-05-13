import os
import random
import zipfile

import numpy as np

from datasetingestion import DatasetIngestion


class StanfordIngestion(DatasetIngestion):
    def decompress(self, images_path, image_filepath):
        if not os.path.exists(images_path):
            print
            "Extracting zip file. It may take a few minutes..."
            with zipfile.ZipFile(image_filepath, "r") as zf:
                zf.extractall(images_path)

    def getClasses(self):
        train_list_path = "./datasets/Stanford/Ebay_train.txt"
        test_list_path = "./datasets/Stanford/Ebay_test.txt"

        train_records = np.loadtxt(train_list_path, np.str, skiprows=1)
        train_labels = train_records[:, 1].astype(np.int)
        train_files = train_records[:, 3]
        test_records = np.loadtxt(test_list_path, np.str, skiprows=1)
        test_labels = test_records[:, 1].astype(np.int)
        test_files = test_records[:, 3]

        images = np.concatenate((train_files, test_files)).tolist()
        class_labels = np.concatenate((train_labels, test_labels)).tolist()
        class_names = [image.split('/')[0].replace('_final','').replace('_',' ') for image in images]

        return images, class_labels, class_names

    def getTestSamples(self, images, class_labels, class_names, num_classes, images_path):
        testClasses = sorted(random.sample(list(np.unique(class_labels)), k=num_classes))
        testIndexes = [index for index, value in enumerate(class_labels) if value in testClasses]
        testImages = [os.path.join(images_path, value) for index, value in enumerate(images) if index in testIndexes]
        testLabels = [value for index, value in enumerate(class_labels) if index in testIndexes]
        testNames = [class_names[label - 1] for label in testLabels]

        return testImages, testLabels, testNames