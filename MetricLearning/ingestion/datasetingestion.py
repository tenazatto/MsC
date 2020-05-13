import os

import cv2
import h5py
import numpy as np
from tqdm import tqdm

from h5pydataset import H5PYDataset


class DatasetIngestion:
    def __init__(self, args, data_path='', images_path='', image_filepath='', hdf5_filename=''):
        self.args = args
        self.data_path = data_path
        self.images_path = images_path
        self.image_filepath = image_filepath
        self.hdf5_filename = hdf5_filename

    def preprocess(self, hwc_bgr_image, size):
        hwc_rgb_image = cv2.cvtColor(hwc_bgr_image, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(hwc_rgb_image, (size))
        chw_image = np.transpose(resized, axes=(2, 0, 1))
        return chw_image

    def hdf5File(self, path, fileName):
        # open hdf5 file
        hdf5_filepath = os.path.join(path, fileName)
        return h5py.File(hdf5_filepath, mode="w"), hdf5_filepath

    def writeDataset(self, hdf5, hdf5_filepath, testImages, testLabels, testNames):
        num_examples = len(testImages)

        # store images
        image_size = (256, 256)
        array_shape = (len(testLabels), 3) + image_size
        ds_images = hdf5.create_dataset("images", array_shape, dtype=np.uint8)
        ds_images.dims[0].label = "batch"
        ds_images.dims[1].label = "channel"
        ds_images.dims[2].label = "height"
        ds_images.dims[3].label = "width"

        # write images to the disk
        for i, filename in tqdm(enumerate(testImages), total=num_examples,
                                desc=hdf5_filepath):
            raw_image = cv2.imread(filename,
                                   cv2.IMREAD_COLOR)  # BGR image
            image = self.preprocess(raw_image, image_size)
            ds_images[i] = image

        # store the targets (class labels)
        targets = np.array(testLabels, np.int32).reshape(num_examples, 1)
        ds_targets = hdf5.create_dataset("targets", data=targets)
        ds_targets.dims[0].label = "batch"
        ds_targets.dims[1].label = "class_labels"

        # specify the splits
        uniqueLabels = list(np.unique(testLabels))
        middleLabel = uniqueLabels[int(np.round(len(uniqueLabels) / 2))]
        test_head = testLabels.index(middleLabel)
        split_train, split_test = (0, test_head), (test_head, num_examples)
        split_dict = dict(train=dict(images=split_train, targets=split_train),
                          test=dict(images=split_test, targets=split_test))
        hdf5.attrs["split"] = H5PYDataset.create_split_array(split_dict)

        hdf5.flush()
        hdf5.close()

    def start(self):
        images, class_labels, class_names = self.getClasses()
        testImages, testLabels, testNames = self.getTestSamples(images, class_labels, class_names, int(self.args.num_classes), self.images_path)

        self.decompress(self.images_path, self.image_filepath)

        hdf5, hdf5_filepath = self.hdf5File(self.data_path, self.hdf5_filename)

        self.writeDataset(hdf5, hdf5_filepath, testImages, testLabels, testNames)


    def decompress(self, images_path, image_filepath):
        pass

    def getClasses(self):
        pass

    def getTestSamples(self, images, class_labels, class_names, num_classes, images_path):
        pass
