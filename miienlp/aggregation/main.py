from aggregation import Aggregation
import utils
import os, argparse
import pandas as pd
import glob

def main(args):
    params = utils.get_params(args['input'])
    df = pd.read_csv('metadata.csv')
    if df.shape[1] == 1: 
        all_files = df["path"].tolist()
        with open("combined_text.txt", "wb") as outfile:
            for f in all_files:
                with open(f, "rb") as infile:
                    outfile.write(infile.read())
    
    else: 
        ag = Aggregation(params['metadata_file'], params["output_dir"])
        if isinstance(params["groups"], list):
            ag.aggregate_lst(params["groups"])
        elif isinstance(params["groups"], dict):
            ag.aggregate_dict(params["groups"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', "--input", required=False, help="Path to input yaml file")
    args = vars(ap.parse_args())
    main(args)
