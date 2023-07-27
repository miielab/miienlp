#########################################################
# author: Ayush Raj
# email: ayushraj@berkeley.edu
# description: categorization of words and sentiment analysis inference using BERT
#########################################################

import os # import various packages here
import utils # importing functions from src/utils.py file
from inference import Inference # use to predict sentiment of sentences
from clean_text import CleanText # replace categorizable words with category names
from clean_text import noCSVException # error for no category csv
import glob # check if there is a category csv

def main():
    """
    Given a sentence, BERT fine-tuned on SST-5 will predict its sentiment
    if a character in the input sentence is identified by demographic information, the script will record that
    """

    # Load the device (GPU if available), model (best-performing bert-base-uncased model), and the tokenizer associated with that model
    device = utils.connect_GPU()
    model, tokenizer = utils.load_model(device)

    params = utils.get_params()

    # if the file pointed to in 'category_dir' is not a csv, raise the noCSVException defined in clean_text
    if len(glob.glob(params['category_dir'] + "/*.csv")) == 0:
        raise noCSVException
    else:
        csv_files = [f for f in os.listdir(params['category_dir']) if f.endswith('.csv')]
        ct = CleanText(category_file=params['category_dir'] + csv_files[0], fuzzy=params['fuzzy'], threshold_fuzzy=params['threshold_fuzzy'], case_sensitive=params['case_sensitive'])

    for root, subdirs, files in os.walk(params['data_dir']): # walking through files in the data directory
        for file in files:
            file_path = os.path.join(root, file)

            # use if statement to avoid grabbing data from .csv file with category information - this was completed earlier
            if file_path.endswith((".txt", "_files")):
                data = utils.load_data(file_path).splitlines() # loading in sentences from the text file and splitting by newline characters
                filename = file.split('/')[-1][:-4] # grabbing the filename of the specific .txt file
                utils.construct_output(params['output_dir']) # constructs output directory, if not already created
                output_file = params['output_dir'] + '/' + filename + '.csv' # creating output file path (based on the name of the given file)
                inf = Inference(data, output_file, model, device, tokenizer, ct)
                inf.create_output()

if __name__ == '__main__':
    main()