from aggregation import Aggregation
import utils
import os, argparse

def main(args):
    params = utils.get_params(args['input'])
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