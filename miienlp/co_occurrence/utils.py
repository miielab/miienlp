import yaml
import os

_curdir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARAMS_FILE = os.path.join(_curdir, 'input.yaml')
DEFAULT_YAML = {
    'text': "",
    'domains': "",
    'groups': "",
    'output': "co_occurrence.csv",
    'method': 'sentence', # sentence or context
    #'temporal': False,
    'window': 4, # if using context window
    'subcats': [],
    'scaled': 'group',
    'difference': True
}

def get_params(params_file=DEFAULT_PARAMS_FILE):
    '''
    Read in parameters from .yaml file
    '''
    with open(params_file, 'r') as stream:
        params = yaml.safe_load(stream)
    params = load_defaults(params, DEFAULT_YAML)
    params = check_params(params)
    return params

def load_defaults(params, DEFAULT_YAML):
    '''
    Loads default values for missing yaml keys/values (i.e. if a user doesn't provide certain parameters in their yaml file.)
    '''
    for key, value in DEFAULT_YAML.items():
        try:
            params[key]
        except:
            params[key] = value
    return params

def check_params(params):
    '''
    Validate user inputs
    '''
    #params["temporal"] = validate_boolean(params["temporal"])
    #if params["temporal"]:
    #    params["text"] = validate_data_dir(params["text"])
    #else:
    params["text"] = validate_text_path(params["text"])
    params["domains"] = validate_data_dir(params["domains"])
    params["groups"] = validate_data_dir(params["groups"])
    params['output'] = validate_output(params['output'])
    params['scaled'] = validate_scaling(params['scaled'])
    # validate method, window, subcats
    return params


def validate_data_dir(data_dir):
    '''
    Checks whether the data directory is valid
    '''
    if os.path.isdir(data_dir):
        return os.path.abspath(data_dir)
    else:
        raise Exception("The directory located at", data_dir, "does not exist. Please specify valid path.")

def validate_output(file):
    '''
    Checks whether the requested output directory is valid
    '''
    if os.path.isdir(os.path.dirname(file)):
        if file[-4:] == ".csv":
            return os.path.abspath(file)
    else:
        print("The directory located at", str(os.path.dirname(file)), "does not exist or file input is not a CSV. Using default output file at test.csv")
        return "test.csv"

def validate_text_path(text):
    '''
    Checks whether the text file path is valid
    '''
    if os.path.isfile(text):
        if text[-4:] == ".txt":
            return os.path.abspath(text)
    else:
        raise Exception("The file located at", text, "does not exist or is not a .txt file. Please specify valid path.")

def validate_scaling(scaled):
    if scaled == False or scaled == "False" or scaled == "false":
        return False
    elif scaled.lower() == "group":
        return scaled.lower()
    elif scaled.lower() == "domain":
        return scaled.lower()
    else:
        raise Exception("The scaling specified does not exist. Please use either False, group, or domain")

def validate_boolean(inp):
    '''
    Makes sure value is a boolean
    '''
    if type(inp) == bool:
        return inp
    else:
        raise Exception(str(inp) + " Should be a boolean: True or False")


def read_sentences(text):
    '''
    Read in a single text file, each sentence as element in list
    '''
    with open(text, 'r') as f:
        input_text = f.readlines()
    return input_text

def read_temporal_sentences(text):
    '''
    Read in multiple text files, where each sentence is an element in a list
    '''
    input_text = {}
    for file in os.listdir(text):
        if file[0:3] == "log":
            continue
        path = text + "/" + file
        decade = file[0:3] + "0"
        input_text[decade] = read_sentences(path)
    return input_text

def read_text(text):
    '''
    Read in a single text file to a string
    '''
    with open(text, 'r') as f:
        input_text = f.read()
    return input_text

def read_temporal_text(text):
    '''
    Read in multiple text files into single string
    '''
    input_text = {}
    for file in os.listdir(text):
        if file[0:3] == "log":
            continue
        path = text + "/" + file
        decade = file[0:3] + "0"
        input_text[decade] = self.read_text(path)
    return input_text

def read_vocab_files(files, subcats):
    '''
    Create list of strings containing either groups or domains
    '''
    d = {}
    for file in os.listdir(files):
        if not subcats or file.split(".")[0] in subcats:
            path = files + "/" + file
            with open(path, 'r') as f:
                vocab = f.read().splitlines()
            d[file.split(".")[0]] = set(vocab)
    return d
