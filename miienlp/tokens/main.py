from miienlp.tokens.counts import Counts
import miienlp.tokens import utils
import glob, os
import pandas as pd
#from alive_progress import alive_bar
import argparse

def main(args):
    params = utils.get_params(args['input'])
    num_files = len(glob.glob(params['data_dir'] + '/**/*.txt', recursive=True))
    specific_words_total_df = pd.DataFrame()

    with alive_bar(num_files, bar="blocks") as bar:
        for root, subdirs, files in os.walk(params['data_dir']):
            for _file in files:
                file_path = os.path.join(root, _file)
                if not file_path.endswith('.txt'): 
                    continue
                data = utils.load_data(file_path)
                filename = _file.split('/')[-1][:-4]
                if data is None:
                    continue

                # running specific words analysis
                if params['specific_words']['output_dir']:
                    output_folder = utils.construct_output_filenames(root, params['data_dir'], params['specific_words']['output_dir'], 'specific_words', filename)
                    output_filename = output_folder + "_word_counts.csv"
                    if not os.path.isfile(output_filename):
                        df_counts = run_sw(data, params, _file, file_path, output_folder)
                        utils.save_results(df_counts, output_filename)
                bar()


def run_sw(data, params, _file, file_path, output_folder=""):
    wc = Counts(data, params['specific_words']['categorize_file'], params['specific_words']['subcats'], params['specific_words']['method'], spacy_dataset=params['specific_words']['spacy_dataset'], _type=params['specific_words']['type'])
    df = wc.run_pipeline(output_folder)
    df.insert(0, "filepath", file_path)
    df.insert(1, "corpus", file_path.split('/')[-3])
    df.insert(2, "book_id", _file[:-4]) 
    df.insert(3, "spacy_dataset", params['ner']['spacy_dataset']) 
    df.insert(4, "total_words", len(data.split()))
    return df

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', "--input", required=False, help="Path to input yaml file")
    args = vars(ap.parse_args())
    main(args)
