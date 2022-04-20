from word_vecs import WordVectors
import utils
from alive_progress import alive_bar
import argparse

def main(args):
    '''
    Runs word vector pipeline
    '''
    params = utils.get_params(args['input']) if args['input'] is not None else utils.get_params()
    print("creating model(s) ...")
    data_dir = params['data_dir']
    if not isinstance(data_dir, list):
        data_dir = [data_dir]
    for model_id in range(params['model']['num_models']):
        print(model_id)
        with alive_bar(len(data_dir), bar="blocks") as bar:
            for path in list(data_dir):
                if path.endswith('.txt'):
                    run_wvec(path, params, model_id)
                    bar()
                else:
                    for root, dirs, files in os.walk(path):
                        for _file in files:
                            if _file.endswith(".txt"):
                                run_wvec(_file, params)
                    bar()
    return

def run_wvec(path, params, model_id):
    wemb = WordVectors(path, params['model'], params['output'], model_id)
    if params['model']['name'] == 'word2vec':
        wemb.make_w2v_model()
    return


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', "--input", required=False, help="Path to input yaml file")
    args = vars(ap.parse_args())
    main(args)

