import argparse
from dataset_readers.spider import SpiderDatasetReader

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--main_path', type=str, default='dataset/', help="Put a link to spider dataset")
    config = parser.parse_args()

    main_path = config.main_path
    tables_file = main_path + "tables.json"
    train_data_path = main_path + "train_spider.json"
    dataset_path = main_path + "database"
    validation_data_path = main_path + "dev.json"

    # Create training dataset
    reader_train = SpiderDatasetReader(tables_file=tables_file, dataset_path=dataset_path, keep_if_unparsable=False)
    train_dataset = reader_train.read(train_data_path)
    # Create validation dataset
    reader_val = SpiderDatasetReader(tables_file=tables_file, dataset_path=dataset_path, keep_if_unparsable=True)
    validation_dataset = reader_val.read(validation_data_path)