from ner import NER
from specific_words import SpecificWordCounts
import utils
import glob, os
import pandas as pd
from alive_progress import alive_bar
import argparse

def main(args):
    params = utils.get_params(args['input'])
    num_files = len(glob.glob(params['data_dir'] + '/**/*.txt', recursive=True))
    NER_total_df = pd.DataFrame(columns=["filepath", "entity", "modal_tag", "person_tag", "freq"])
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

                # running NER analysis
                if params['ner']['output_dir']:
                    output_folder = utils.construct_output_filenames(root, params['data_dir'], params['ner']['output_dir'], 'ner', filename)
                    filter_keywords = "_".join(params['ner']['filter_entities'])
                    output_filename = output_folder + "_" + filter_keywords + "_NER_counts.csv"
                    if not os.path.isfile(output_filename):
                        df = run_ner(data, params, _file, file_path)
                        utils.save_results(df, output_filename)
                        #NER_total_df = NER_total_df.append(df) #uncomment this when we want a combined NER dataset (emileigh)

                # running specific words analysis
                if params['specific_words']['output_dir']:
                    output_folder = utils.construct_output_filenames(root, params['data_dir'], params['specific_words']['output_dir'], 'specific_words', filename)
                    output_filename = output_folder + "_word_counts.csv"
                    if not os.path.isfile(output_filename):
                        df_counts = run_sw(data, params, _file, file_path, output_folder)
                        utils.save_results(df_counts, output_filename)
                bar()
            # add below codeblock back in when we want to have a large combined NER dataset (emileigh)
            '''
            if params['ner']['output_dir']:
                NER_total_df.reset_index(drop=True, inplace=True)
                total_output = params['ner']['output_dir'] + '/ner/'
                utils.construct_output(total_output)
                utils.save_results(NER_total_df, total_output + 'NER_combined.csv')
            '''

def run_ner(data, params, _file, file_path):
    ner = NER(data, params['ner']['filter_entities'], params['ner']['spacy_dataset'])
    df = ner.run_pipeline()
    df.insert(0, "filepath", file_path) 
    df.insert(1, "corpus", file_path.split('/')[-3])
    df.insert(2, "book_id", _file[:-4])
    df.insert(3, "spacy_dataset", params['ner']['spacy_dataset']) 
    return df

def run_sw(data, params, _file, file_path, output_folder=""):
    swc = SpecificWordCounts(data, params['specific_words']['categorize_file'], params['specific_words']['subcats'], params['specific_words']['method'], spacy_dataset=params['specific_words']['spacy_dataset'], _type=params['specific_words']['type'])
    df = swc.run_pipeline(output_folder)
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
