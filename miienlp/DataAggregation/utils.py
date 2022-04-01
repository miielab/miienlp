import os, yaml 
import pandas as pd

_curdir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARAMS_FILE = os.path.join(_curdir, 'input.yaml')

DEFAULT_YAML = {
'output_dir': os.getcwd() + "/combined/"
}

def get_params(params_file=DEFAULT_PARAMS_FILE, args=None):
    '''
    Reads in user input parameters from input.yaml file and processes information
    '''
    with open(params_file, 'r') as stream:
        params = yaml.safe_load(stream)
    params = check_params(params)
    load_defaults(params, DEFAULT_YAML)
    return params

def check_params(params):
    '''
    Validates necessary parameters
    '''
    params["metadata_file"] = validate_metadata_path(params["metadata_file"])
    validate_groups(params)
    return params

def validate_groups(params):
    '''
    Validates whether specified groups match column values in metadata CSV
    '''
    columns = set(pd.read_csv(params["metadata_file"]).columns)
    groups = params["groups"]
    if isinstance(groups, dict):
        for key, values in groups.items():
            for value in values:
                if value not in columns: raise Exception("Your specified group column names from your input.yaml file must match a column in {}".format(params["metadata_file"]))
    elif isinstance(groups, list):
        for values in groups:
            for value in values:
                if value not in columns: raise Exception("Your specified group column names from your input.yaml file must match a column in {}".format(params["metadata_file"]))
    return

def validate_metadata_path(metadata):
    '''
    Checks whether the data directory is valid
    '''
    if os.path.isfile(metadata):
        if metadata.endswith(".csv"):
            return os.path.abspath(metadata)
        else:
            raise Exception("Your metadata file located at {} must be in .csv format.".format(metadata)) 
    else:
        raise Exception("The metadata file located at {} does not exist. Please specify valid path.".format(metadata))   

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

def save_output(text, output_filename):
    """
    Writes string to output file
    """
    with open(output_filename, 'w+') as outfile:
        outfile.write(text)
        outfile.close()

def makedir(output_dir):
    """
    Creates output directory
    """
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
