import yaml
import os
import shutil
import cv2

_curdir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARAMS_FILE = os.path.join(_curdir, 'input.yaml')
DEFAULT_YAML = {
    'raw_data_directory': "",
    'output_directory': "", # path to desired output, default is /path/to/raw/../ocr_output
    'ocr_method': "Google Vision", # Google Vision or Tesseract (Tesseract not yet working)
    'confidence_threshold': 0.5, # Value between 0 and 1, inclusive
    'image_ordering': "underscore_numerical", # order: page_1.jpg, page_2.jpg, page_3.jpg
    'language': [], # list of languages in text. eg: ["English", "Spanish"]
    'project_id': "", # google vision project id
    'model_id': "", # google vision single label model id
    'remove_cover_ends': False, # whether or not to remove cover and end pages from text using AutoML
    'preprocess_images': False
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
            if key != "output_directory" and key != "language" and key != "double_scans": 
                print(key + " not provided. Using default = " + str(value))
            params[key] = value
    return params

def check_params(params):
    '''
    Validate user inputs
    '''
    params["raw_data_directory"] = validate_data_dir(params["raw_data_directory"])
    params["ocr_method"] = validate_method(params["ocr_method"])
    params["image_ordering"] = validate_ordering(params["image_ordering"])
    params["output_directory"] = validate_create_output_dir(params["output_directory"], params["raw_data_directory"])
    params["confidence_threshold"] = validate_confidence(params["confidence_threshold"])
    params["language"] = validate_language(params["language"])
    params["remove_cover_ends"] = validate_boolean(params["remove_cover_ends"])
    params["preprocess_images"] = validate_boolean(params['preprocess_images'])
    # add validations for project and model id
    return params

def validate_data_dir(data_dir):
    '''
    Checks whether the data directory is valid
    '''
    if os.path.isdir(data_dir):
        return os.path.abspath(data_dir)
    else:
        raise Exception("The directory located at", data_dir, "does not exist. Please specify valid path.")

def validate_create_output_dir(output_dir, input_dir):
    '''
    If desired output directory is not provided or its path is not defined, use default output directory
    of /path/to/raw_data_dir/../ocr_output
    '''
    if os.path.exists(os.path.dirname(output_dir +".txt")):
        return os.path.abspath(output_dir)
    elif output_dir == "":
        print("No output directory specified. Using default /path/to/raw_data_dir/../ocr_output")
    else:
        print("Specified path does not exist. Using default /path/to/raw_data_dir/../ocr_output")
    output = os.path.abspath(os.path.join(input_dir, "../..")) + "/ocr_output"
    construct_filepaths(output)
    return output

def validate_method(ocr_method):
	'''
	Makes sure the OCR method is either Tesseract or Google Vision
	'''
	if ocr_method == "Tesseract" or ocr_method == "Google Vision":
		return ocr_method
	else:
		raise Exception("The OCR method does not exist or is not available. Please specify either Tesseract or Google Vision")
	
def validate_ordering(order):
    '''
    Validates that the image order type provided by the user is allowed
    '''
    if order == "alphabetical" or order == "numerical" or order == "underscore_numerical" or order == "dash_numerical":
        return order
    else:
        raise Exception("The image ordering does not exist or is not available. Please specify alphabetical, numerical, underscore_numerical, or dash_numerical")


def validate_confidence(threshold):
    '''
    Validates that the confidence provided by the user is a value between [0,1]
    '''
    if not (type(threshold) == float or type(threshold) == int):
        raise Exception("Threshold value must be an integer or decimal value from [0,1]")
    elif threshold < 0 or threshold > 1:
        raise Exception("Threshold vallue must be an integer or decimal valule from [0,1]")
    else:
        return threshold

def validate_language(lang):
    '''
    Validates language input from user
    '''
    if type(lang) != list:
        raise Exception("Language parameter must be a list of strings. For example, ['English']")
    if lang == []:
        print("No language inputted. Allowing auto-language detection")
        return []
    ls = []
    for l in lang:
        if l == "English":
            ls.append("en")
        elif l == "Spanish":
            ls.append("es")
        elif l == "Hindi":
            ls.append("hi")
        elif l == "Chinese":
            ls.append("zh")
        else:
            raise Exception("Language does not exist or is not included here. Possible languages include English, Spanish, Chinese, and Hindi.")
    return ls



def validate_boolean(cover_end):
    '''
    Makes sure value is a boolean
    '''
    if type(cover_end) == bool:
        return cover_end
    else:
        raise Exception(str(cover_end) + " Should be a boolean: True or False")


def construct_filepaths(directory):
    '''
    Constructs filepaths for the cleaned data
    '''
    if not os.path.isdir(directory):
        os.mkdir(directory)	

def remove_temp(directory):
    '''
    Removes temporary directory and all of its contents
    '''
    try:
        shutil.rmtree(directory)
        print("Removed temporary directory " + directory)
    except OSError as e:
        print("Error: %s : %s" % (directory, e.strerror))

def validate_scan(file):
    '''
    Validates that the scan can be read and manipulated
    '''
    try:
        img = cv2.imread(file)
        img.shape
        return file
    except:
        print("unable to open image: ", file)
        return None




