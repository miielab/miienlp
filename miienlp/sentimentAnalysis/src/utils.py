import yaml, os, torch, pickle
import pandas as pd
from transformers import AutoModel, AutoTokenizer
from bert_classifier import BertClassifier

_curdir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARAMS_FILE = os.path.join(_curdir, 'input.yaml') # looks for input.yaml file in src/ directory

### Loads in input.yaml file ###
def get_params(params_file=DEFAULT_PARAMS_FILE, args=None):
    with open(params_file, 'r') as stream:
        params = yaml.safe_load(stream)
    params = check_params(params)
    return params

### Performs checks on user input parameters ###
def check_params(params):
    params["data_dir"] = validate_data_dir(params["data_dir"])
    # note: you can add extra checks in this function to check whether certain files are of the correct format etc.
    return params

### Checks whether input data directory is valid ###
def validate_data_dir(data_dir):
    if os.path.isdir(data_dir):
        return os.path.abspath(data_dir)
    else:
        raise Exception("The directory located at", data_dir, "does not exist. Please specify valid path.")
    
### Loads in text file and returns None if it was unable to be opened. This is called in src/main.py ###
def load_data(data_file):
    try:
        with open(data_file, 'r') as infile:
            return infile.read()
    except:
        print("unable to open file:", data_file)
        return None

### If your code is outputing results somewhere, makes sure this folder(s) exists already and if not, creates them ###
def construct_output(output_dir):
    '''
    Constructs output directories
    '''
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    return 1

### Connect to a GPU if one is available for improved computation speeds ###
def connect_GPU():
    if torch.cuda.is_available():       
        device = torch.device("cuda")
        print(f'There are {torch.cuda.device_count()} GPU(s) available.')
        print('Device name:', torch.cuda.get_device_name(0))
    else:
        device = torch.device("cpu")
        print('No GPU available, using the CPU instead.')
    return device

### Loads the best-performing bert-base-uncased model ###
def load_model(device):
    # load a model
    model = BertClassifier()
    model.load_state_dict(torch.load('../model/model_save_testing.pt', map_location=device))
    
    # load a tokenizer
    tokenizer = AutoTokenizer.from_pretrained('../model/bert-base-uncased')

    return model, tokenizer

### Loads file with words to be categorized. File must be a .csv
def load_categorize_file(categorize_file):
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