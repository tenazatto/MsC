import argparse

from Cars196Ingestion import Cars196Ingestion
from CUB2002011Ingestion import CUB2002011Ingestion
from StanfordIngestion import StanfordIngestion

parser = argparse.ArgumentParser(description='Dataset ingestion')
parser.add_argument('-n', '--num-classes', dest='num_classes',
                    help='number of dataset classes', default=50)
parser.add_argument('-d', '--dataset', dest='dataset',
                    help='dataset type', default='cars196')

if __name__ == '__main__':
    args = parser.parse_args()

    if args.dataset == "cars196":
        Cars196Ingestion(
            args,
            data_path='../datasets/cars196/data',
            images_path='../datasets/cars196/images',
            image_filepath='../datasets/cars196/car_ims.tgz',
            hdf5_filename='cars196.hdf5'
        ).start()
    elif args.dataset == "CUB":
        CUB2002011Ingestion(
            args,
            data_path='../datasets/CUB/data',
            images_path='../datasets/CUB/images',
            image_filepath='../datasets/CUB/CUB_200_2011.tgz',
            hdf5_filename='CUB2002011.hdf5'
        ).start()
    else:
        StanfordIngestion(
            args,
            data_path='../datasets/Stanford/data',
            images_path='../datasets/Stanford/images',
            image_filepath='../datasets/Stanford/Stanford_Online_Products.zip',
            hdf5_filename='Stanford.hdf5'
        ).start()


