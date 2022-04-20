import yaml
import os


_curdir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARAMS_FILE = os.path.join(_curdir, 'input.yaml')

DEFAULT_YAML = {
'ner':
  {'spacy_dataset': 'en_core_web_sm',
  'filter_entities': [],
  'output_dir': ''
  },
'specific_words': 
  {'categorize_file': None,
    'spacy_dataset': 'en_core_web_sm',
    'method': 'nltk',
    'subcats': [],
    'type': 'LU',
    'output_dir': ''
  }
}

def get_params(params_file=DEFAULT_PARAMS_FILE, args=None):
    '''
    Reads in user input parameters from input.yaml file and processes information
    '''
    with open(params_file, 'r') as stream:
        params = yaml.safe_load(stream)
    params = check_params(params)
    load_defaults(params, DEFAULT_YAML)
    #download_pkgs(params['ner']['dataset']) commenting out because this cannot be run on compute nodes
    return params

def check_params(params):
    '''
    Validates neecessary parameters
    '''
    params["data_dir"] = validate_data_dir(params["data_dir"])
    return params

def download_pkgs(ner_type):
    '''
    Attempts to download necessary spacy packages
    Note: this function will not work on compute nodes on Midway
    '''
    try:
        print("attempting to download necessary packages ...")
        download = "python -m spacy download " + ner_type
        os.system(download)
        print("successfully downloaded necessary spacy packages!")
    except:
        raise Exception("Unable to download necessary SpaCy packages")
        return 0
    return 1

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

def validate_data_dir(data_dir):
    '''
    Checks whether the data directory is valid
    '''
    if os.path.isdir(data_dir):
        return os.path.abspath(data_dir)
    else:
        raise Exception("The directory located at", data_dir, "does not exist. Please specify valid path.")

def load_data(data_file):
    '''
    Opens clean text file and returns data string
    '''
    try:
        with open(data_file, 'r') as infile:
            return infile.read()
    except:
        print("unable to open file:", data_file)
        return None

def construct_output(output_dir):
    '''
    Constructs output directories
    '''
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    return 1

def construct_output_filenames(root, data_dir, output_dir, method, filename):
    '''
    Constructs specific output files
    '''
    output_dir = output_dir + '/' + method + '/' + root[len(data_dir):] #COMMENT BACK IN WHEN DATA/ FOLDER IS UPDATED
    output_filename = output_dir + '/' + filename
    construct_output(output_dir)
    return output_filename

def save_results(df, output_file, index=False):
    '''
    Saves results to csv file
    '''
    df.to_csv(output_file, index=index)
    return 1

def determine_data_dir_structure(data_dir):
    '''
    Determines whether a user has organized their data by collection and/or time series
    '''
    structure = []
    for root, subdirs, files in os.walk(data_dir):
        if not subdirs and files:
            structure.append("data")
            return structure
        if not subdirs and not files:
            raise Exception("No data was found."); return None
        if subdirs[0].isnumeric():
            structure.append("time_series")
        else:
            structure.append("collections")


def read_vocab_files(_dir, subcats, _type):
    '''
    Create list of strings containing either genders or domains
    '''
    subcats = [cat + '.txt' for cat in subcats] if subcats else []
    d = {}
    for root, subdir, files in os.walk(_dir):
        for _file in files:
            if subcats and _file.endswith('.txt') and _file in subcats:
                d = construct_vocab_dict(d, root, _file, _type)
            elif not subcats and _file.endswith('.txt'):
                d = construct_vocab_dict(d, root, _file, _type)
    return d

def construct_vocab_dict(d, root, _file, _type):
    '''
    Creates dictionary of specific word construct and related words
    '''
    vocab_set = set()
    path = os.path.join(root, _file)
    try:
        with open(path, 'r') as f:
            vocab = f.read().splitlines()
            for word in vocab:
                if _file.split(".")[0] == "male_pronouns_lower" or _file.split(".")[0]  == "female_pronouns_lower":
                    vocab_set.add(word.lower())
                elif _file.split(".")[0] == "male_pronouns_upper" or _file.split(".")[0]  == "female_pronouns_upper":
                    vocab_set.add(word.capitalize())
                elif _type == "L":
                    vocab_set.add(word.lower())
                elif _type == "U":
                    vocab_set.add(word.capitalize())
                else:
                    vocab_set.update([word.lower(), word.capitalize()])

        d[_file.split(".")[0]] = vocab_set
        return d
    except FileNotFoundError:
        print("Warning: the filepath", path, "was not able to be opened.")