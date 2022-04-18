from itertools import combinations
import argparse, os
import gensim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compute_variance(group1, group2, n):
    '''
    Computes the variance between two groups of words
    '''
    return 1 - len(find_intersection(group1, group2)) / n

def find_intersection(group1, group2):
    '''
    Finds intersection between two groups of words
    '''
    return list(group1 & group2)

def find_top_n_similar(word, model, n=25):
    '''
    Finds top n most similiar words to a given target word
    '''
    # TO DO: does order matter? if it does, we should not make set
    top_n_words = []
    words = model.most_similar(word, topn=n) if word in model.vocab else []
    for word in words:
        top_n_words.append(word[0])
    return set(top_n_words)

def load_model(_file):
    '''
    Loads in the word2vec model
    '''
    return gensim.models.KeyedVectors.load_word2vec_format(_file, binary=True)

def generate_combinations(models):
    '''
    Generates all combinations of two model paths
    '''
    return list(combinations(models, 2))

def read_vocab_files(dir, subcats):
    '''
    Create list of strings containing either genders or domains
    '''
    d = {}
    subcats = [cat + '.txt' for cat in subcats]
    for root, subdir, files in os.walk(dir):
        for _file in files:
            if _file.endswith('.txt') and _file in subcats:
                path = os.path.join(root, _file)
                try:
                    with open(path, 'r') as f:
                        vocab = f.read().splitlines()
                        vocab = list(map(lambda x: x.replace(" ", "_"), vocab))
                    d[_file.split(".")[0]] = set(vocab)
                except FileNotFoundError:
                    print("Warning: the filepath", path, "was not able to be opened.")
    return d

def generate_target_word_dict(model_dir, categorize_file=None):
    '''
    Generates target word dictionary of {'race_gender':word}, where word is either a famous person name (unbundled) or 'white_female' (bundled)
    '''
    if model_dir.split('/')[-2] == "bundled":
        return {'black_female':['black_female'], 'black_male':['black_male'], 'white_female':['white_female'], 'white_male':['white_male']}
    else:
        return read_vocab_files(categorize_file, ['black_female', 'black_male', 'white_male', 'white_female'])

def find_variance(variance, d, model_combinations, n, bundle_type):
    '''
    Computes variance for all race_gender categories
    '''
    for race_gender, word_lst in d.items():
        for word in word_lst:
            for pair in model_combinations:
                model1_words = find_top_n_similar(word, pair[0], n)
                model2_words = find_top_n_similar(word, pair[1], n)
                var = compute_variance(model1_words, model2_words, n)
                if var != 1.0:
                    variance.append([var, race_gender, bundle_type, word])
    return variance

def find_model_combinations(model_dir):
    '''
    Given a model path, finds all possible model combinations
    '''
    model_paths = map(lambda name: os.path.join(model_dir, name), os.listdir(model_dir))
    models = [load_model(model) for model in model_paths]
    return generate_combinations(models)

def main(model_dirs, n, categorize_file=None, plot=True):
    variance = []
    for model_dir in model_dirs:
        model_combinations = find_model_combinations(model_dir)
        target_words_dict = generate_target_word_dict(model_dir, categorize_file)
        model_type = '_'.join(model_dir.split('/')[-2:])
        variance = find_variance(variance, target_words_dict, model_combinations, n, model_type)

    df = pd.DataFrame(variance, columns=['variance', 'race_gender', 'bundle_type', 'name'])
    df.to_csv('variance_n{}.csv'.format(n))
    

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', "--model_path", required=False, help="Path to model directory")
    args = ap.parse_args()
    model_path = ['/project2/adukia/miie/text_analysis/models/simulation/bundled/mainstream', '/project2/adukia/miie/text_analysis/models/simulation/unbundled_all_famous/mainstream',
    '/project2/adukia/miie/text_analysis/models/simulation/bundled/diversity', '/project2/adukia/miie/text_analysis/models/simulation/unbundled_all_famous/diversity']
    #model_path = ['/project2/adukia/miie/text_analysis/models/simulation/bundled/diversity', '/project2/adukia/miie/text_analysis/models/simulation/bundled/mainstream']
    main(model_path, 25, categorize_file='/project2/adukia/miie/text_analysis/supplemental_data/Categories')
