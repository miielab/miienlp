import yaml
import os, sys
import nltk
from nltk.corpus import stopwords
nltk.data.path.append("/project2/adukia/miie/text_analysis/dependencies/text_cleaning/text_cleaning/lib/python3.7/site-packages/nltk_data")
import pandas as pd

_curdir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARAMS_FILE = os.path.join(_curdir, 'input.yaml')
DEFAULT_YAML = {
    'n_gram_file': '',
    'lemmatize': False,
    'stopwords_file': '',
    'categorize_domain':{
        'directory': '',
        'subcats': [],
        'case_sensitive': False},
    'categorize_famous':{
        'fuzzy': True,
        'threshold_fuzzy': 0.9,
        'directory': '',
        'subcats': []},
    'spacy_ner_dataset': None, # we use 'en_core_web_lg' for famous and SSA
    'standardize_file': None,
    'gender_ssa_file': '',
    'digits': False,
    'output_directory': '',
    'stopwords_add': [],
    'stopwords_remove': [],
    'lower': False,
    'special_characters': False
}


def get_params(params_file=DEFAULT_PARAMS_FILE):
    print(params_file)
    with open(params_file, 'r') as stream:
        params = yaml.safe_load(stream)
    load_defaults(params, DEFAULT_YAML)
    params = check_params(params)
    return params

## TO DO: ADD A LOT MORE CHECKING OF PARAMETERS

def check_params(params):
    # TO DO: Make this better at printing errors when they exist
    params["raw_data_directory"] = validate_paths(params["raw_data_directory"])
    if params["n_gram_file"]: params["n_gram_file"] = validate_paths(params["n_gram_file"])
    if params["stopwords_file"]: params["stopwords_file"] = validate_paths(params["stopwords_file"])
    if params["categorize_domain"]["directory"]: params["categorize_domain"]["directory"] = validate_paths(params["categorize_domain"]["directory"])
    if params["categorize_famous"]["directory"]: params["categorize_famous"]["directory"] = validate_paths(params["categorize_famous"]["directory"])
    if params["standardize_file"]: params["standardize_file"] = validate_paths(params["standardize_file"])
    if params["gender_ssa_file"]: params["gender_ssa_file"] = validate_paths(params["gender_ssa_file"])
    return params


def validate_paths(path):
    '''
    Checks whether the data directory or path is valid
    '''
    if os.path.isdir(path) or os.path.isfile(path):
        return os.path.abspath(path)
    else:
        raise Exception("The file or directory located at", path, "does not exist. Please specify valid path.")
        sys.exit()


def load_defaults(params, DEFAULT_YAML, parent_key=''):
    '''
    Loads default values for missing yaml keys/values (i.e. if a user doesn't provide certain parameters in their yaml file.)
    '''
    for key, value in DEFAULT_YAML.items():
        if type(value) is dict:
            load_defaults(params, value, key)
        else:
            try:
                params[parent_key][key] if parent_key else params[key]
            except:
                if parent_key:
                    if parent_key not in params.keys():
                        params[parent_key] = {}
                    params[parent_key][key] = value
                else:
                    params[key] = value
    return

def construct_output_filepaths(out_dir):
    '''
    Constructs output filepaths for the cleaned data
    '''
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

def read_data(file_path):
    '''
    Reads in raw text data from txt file
    '''
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except:
        print("unable to open file:", file_path)
        return None


def load_nltk_pkgs():
    '''
    Looks to see if required nltk packages are installed, if not, installs them for user
    '''
    print("downloading necessary packages...")
    try:
        nltk.data.find("tokenizers/punkt")
    except:
        nltk.download("punkt")
    try:
        nltk.data.find("corpora/stopwords") #stopwords
    except:
        nltk.download("stopwords")
    try:
        nltk.data.find("taggers/averaged_perceptron_tagger")
    except:
        nltk.download("averaged_perceptron_tagger")
    try:
        nltk.data.find("corpora/wordnet") # lemmatization
    except:
        nltk.download("wordnet")

def load_custom_stopwords(stopwords_txt):
    '''
    Loads in custom stopwords file
    '''
    try:
        with open(stopwords_txt, 'r') as f:
            custom_stopwords = set(list(f.read().split('\n')));
            if "" in custom_stopwords: custom_stopwords.remove("") #empty lines in stopwords file
            return custom_stopwords
    except FileNotFoundError:
        print("Warning: the filepath ", stopwords_txt, "was not found. Using default stopwords list from nltk.")
    return set(stopwords.words('english'))

def load_ngram_file(ngram_file):
    '''
    Loading in interesting ngrams file (if it exists) containing words we want combined to one word for contextual word vector analysis
    Example: "Martin Luther King Junior" -> "martin_luther_king_junior"
    '''
    try:
        with open(ngram_file, 'r') as f:
            ngram_lst = list(f.read().lower().split('\n'))
            if "" in ngram_lst: ngram_lst.remove("") #empty lines in ngrams file
            return ngram_lst
    except FileNotFoundError:
        print("Warning: the filepath", ngram_file, "was not found or not specified.")
    return []

def load_ssa_file(ssa_file):
    '''
    Loading in interesting gender social security dataset (if it exists) containing names and classified gender
    Example: "Sophia" -> "Female"
    '''
    try:
        return pd.read_csv(ssa_file, sep=",", engine="python")
    except FileNotFoundError:
        print("Warning: the filepath", ssa_file, "was not found or not specified.")
    return None

def load_standardize_file(standardize_file):
    '''
    Loads file with words to be categorized
    Example: all versions of MLK -> "Martin Luther King Junior"
    '''
    try:
        return pd.read_csv(standardize_file, sep=", ")
    except FileNotFoundError:
        print("Warning: the filepath", standardize_file, "was not found.")
    return None

def load_categorize_file(categorize_file, subcats):
    '''
    Loads file with words to be categorized
    Example: girl -> female
    '''
    # TO DO: throw a specific error if they do not have the correct columnn names ('Specific_Word', 'Category')
    if categorize_file.endswith('.csv'):
        try:
            categorize = {}
            categorize_df = pd.read_csv(categorize_file, sep=",", engine="python")
            grouped_df = categorize_df.groupby("Category")
            for group_name in grouped_df.groups:
                categorize[group_name] = set(grouped_df.get_group(group_name)['Specific_Word'].tolist())
            return categorize
        except FileNotFoundError:
            print("Warning: the filepath", categorize_file, "was not found or column names are incorrect.")
            return
    else:
        subcats = [cat + '.txt' for cat in subcats]
        return read_vocab_files(categorize_file, subcats)

def read_vocab_files(dir, subcats):
    '''
    Create list of strings containing either genders or domains
    '''
    d = {}
    for root, subdir, files in os.walk(dir):
        for _file in files:
            if _file.endswith('.txt') and _file in subcats:
                path = os.path.join(root, _file)
                try:
                    with open(path, 'r') as f:
                        vocab = f.read().splitlines()
                    d[_file.split(".")[0]] = set(vocab)
                except FileNotFoundError:
                    print("Warning: the filepath", path, "was not able to be opened.")
    return d
