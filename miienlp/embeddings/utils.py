import yaml
import os

_curdir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARAMS_FILE = os.path.join(_curdir, 'input.yaml')
DEFAULT_YAML = {
'time_series': {
        'type': 'full',
        'time_frame': 'all'
        },
'collection_corpora': {
        'name':[]
        },
'model': {
        'name': 'word2vec',
        'num_models': 1,
        'size': 300,
        'window': 5,
        'min_count': 10,
        'workers': 5,
        'sg': 1,
        'hs': 1,
        'negative': 0,
        'epochs': 5
        },
'output': {
        'output_model_dir': '',
        'save_vocab_np': False,
        'save_vocab_txt': False
        }
}

def get_params(params_file=DEFAULT_PARAMS_FILE, args=None):
    '''
    Loads in input YAML file and returns user inputs as dictionary
    '''
    with open(params_file, 'r') as stream:
        params = yaml.safe_load(stream)
    params = check_params(params)
    load_defaults(params, DEFAULT_YAML)
    if not params['output']['output_model_dir']:
        # creating default output folder based on input data_dir folder
        params['output']['output_model_dir'] = '/'.join(params['data_dir'].split('/')[:-2]) + '/'
    return params

def check_params(params):
    '''
    Checks whether filepaths or parameter values are valid
    '''
    for data in params["data_dir"]:
        validate_data_path(data)
    return params

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
                    if parent_key == 'collection_corpora':
                        params[parent_key].pop('name')
                else:
                    params[key] = value
    return

def validate_data_path(data_dir):
    '''
    Checks whether the data directory is valid
    '''
    if os.path.isfile(data_dir):
        return os.path.abspath(data_dir)
    else:
        raise Exception("The directory located at", data_dir, "does not exist. Please specify valid path.")

def construct_output_dir(dir):
    '''
    Constructs models folder
    '''
    if not os.path.isdir(dir):
        os.makedirs(dir)
