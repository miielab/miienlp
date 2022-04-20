import argparse
import sys, os
import yaml


# establish user inputs
ap = argparse.ArgumentParser()
ap.add_argument('-a', "--analysis_type", required=True, help="Type of analysis: co-occurrence, token-counts, ner, word-embeddings")
ap.add_argument('-i', '--input_text', required=True, help = "Path to directory or file of raw text")
ap.add_argument('-o', '--yaml_output', required=False, help = "Path to output yaml configuration file")
ap.add_argument('-t', '--clean_output', required = False, help = "Path to output clean text")
args = vars(ap.parse_args())


# input yaml files for each type of analysis
SIMPLE_CLEAN = {'raw_data_directory': args['input_text'], 'digits': True, 'lower': False, 'output_directory': args['clean_output']}
WORD_EMBEDDINGS = {'raw_data_directory': args['input_text'], 'digits': True, 'lower': True, 'special_characters': True, 'output_directory': args['clean_output']}

def validate_data_dir(data_dir):
    '''
    Checks whether the data directory is valid
    '''
    if os.path.isdir(data_dir):
        return os.path.abspath(data_dir)
    else:
        raise Exception("The directory located at", data_dir, "does not exist. Please specify valid path.")
    return

def check_args(args):
    '''
    Checks whether user arguments are valid
    '''
    validate_data_dir(args['input_text'])
    # TO DO: check output directories
    possible_analysis = set(['co-occurrence', 'token-counts', 'ner', 'word-embeddings'])
    if args['analysis_type'] not in possible_analysis:
        raise Exception("The analysis type must be one of the following: co-occurrence, token-counts, ner, word-embeddings")
    return 

def main():
    '''
    Automatically creates YAML file based on the type of analysis a user wants to do.
    '''
    check_args(args)
    if args['yaml_output']:
        _file = open(args['yaml_output'], 'w+')
    else:
        # TO DO: move default somewhere else?
        _file = open('input.yaml', 'w+')
    analysis_type = args['analysis_type'].lower() 
    if analysis_type == 'token-counts' or analysis_type == 'ner':
        # TO DO: right now when the info is dumped it is saved in a different order than specified in simple_clean etc. might want to change this
        yaml.dump(SIMPLE_CLEAN, _file, allow_unicode = True) 
    elif analysis_type == 'word-embeddings' or analysis_type == 'co-occurrence':
        yaml.dump(WORD_EMBEDDINGS, _file, allow_unicode = True)
    return

if __name__ == "__main__":
    main()
    print("-------- Configuration File Successfully Created --------")
