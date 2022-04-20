import utils
import argparse
from co_occurrence import Co_Occurrence


ap = argparse.ArgumentParser()
ap.add_argument('-i', "--input", required=False, help="Path to input yaml file")
args = vars(ap.parse_args())

def main():
    '''
    Runs Co-occurrence pipeline
    '''
    try:
        input_yml = args['input']
        params = utils.get_params(input_yml)
    except:
        params = utils.get_params()

    co = Co_Occurrence(params["text"], params["groups"], params["domains"], params["output"], 
                       params["method"], params["window"], params['subcats'], params['scaled'], params['difference'])
    co.run_cooccurrence()
    return

if __name__ == "__main__":
    main()
