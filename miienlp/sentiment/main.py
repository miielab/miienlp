from fine_tuning import Preprocess, FineTuneBert
import utils import *
import argparse
import numpy as np

def main(args):
    '''
    Runs sentiment pipeline
    '''
    device = determine_core_type() # from utils, determines CPU or GPU
    train_df, val_df, test_df = load_datasets(args['fine_tuning'])
    max_sent = determine_max_sent_len(train_df, val_df, test_df)

    X_train, X_val, X_test = \
        np.array(train_df.sentence), np.array(val_df.sentence), np.array(test_df.sentence)
    y_train, y_val, y_test = \
        np.array(train_df.sentiment_label), np.array(val_df.sentiment_label), np.array(test_df.sentiment_label)
    y_train, y_val, y_test = reformat_sentiment_lbls(y_train, y_val, y_test)

    # preparing data according to BERT standards in fine_tuning.Preprocess class
    train_dataloader = Preprocess(,X_train, y_train).preprocess()
    val_dataloader = Preprocess(X_val, y_val).preprocess()
    test_dataloader = Preprocess(X_test, y_test).preprocess()

    ftb = FineTuneBert()
    # initialize model
    ftb.initialize_model()
    # fine-tune model
    model = ftb.train()
    # evaluate
    model = ftb.evaluate()
    # save model
    ftb.save_model()
    return

def load_datasets(paths):
    '''
    Loads training, testing, validation datasets
    '''
    return load_data(paths['train_data_path'], paths['val_data_path'], paths['test_data_path'])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', "--input", required=False, help="Path to input yaml file")
    args = vars(ap.parse_args())
    main(args)