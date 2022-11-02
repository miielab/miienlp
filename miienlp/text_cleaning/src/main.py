import json, argparse
from clean_text import CleanText
import utils
import os

ap = argparse.ArgumentParser()
ap.add_argument('-i', "--input", required=False, help="Path to input yaml file")
args = vars(ap.parse_args())


def main():
	try: params = utils.get_params(args['input'])
	except: params = utils.get_params()
	print("The following user inputs will be used:")
	print(params)
	categorize_domain = params['categorize_domain']
	categorize_famous = params['categorize_famous']
	print("Running Text Cleaning Pipeline...")
	data_dir = params['raw_data_directory']
	clean_text = CleanText("", ngram_file=params["n_gram_file"], lemmatize=params["lemmatize"], 
							stopwords_file=params["stopwords_file"], 
							categorize_domain_file = categorize_domain['directory'], categorize_domain_subcats = categorize_domain['subcats'],
							fuzzy = categorize_famous['fuzzy'], threshold_fuzzy = categorize_famous['threshold_fuzzy'],
							categorize_famous_file = categorize_famous['directory'], categorize_famous_subcats = categorize_famous['subcats'],
							standardize_file=params["standardize_file"], gender_ssa_file = params["gender_ssa_file"],
							digits=params['digits'], stopwords_add=params['stopwords_add'],
							stopwords_remove=params['stopwords_remove'], lower=params['lower'], special_characters = params["special_characters"],
							spacy_dataset_type = params['spacy_ner_dataset'], case_sensitive = categorize_domain['case_sensitive'])


	# set output directories / filenames if not provided
	output_filename = set_output_file(params["output_directory"], data_dir)

	for root, subdirs, files in os.walk(data_dir):
		output_structure = output_filename + root[len(data_dir):]
		utils.construct_output_filepaths(output_structure)
		for _file in files:
			file_path = os.path.join(root, _file)
			data = utils.read_data(file_path)
			if data is None:
				continue
			output_clean_text_file = output_filename + "".join(file_path.rsplit(data_dir))
            # if clean file already exist, then continue to next raw file
			if os.path.exists(output_clean_text_file):
				continue
			# TO DO: make this extensible based on what type of analysis you are doing
			clean_text.raw_text = data
			clean_text.clean_text_file(output_clean_text_file)
	return 0

def set_output_file(output_filename, data_dir):
	if output_filename == "":
		root_dir_lst = data_dir.split('/')
		root_dir_lst.pop()
		root_dir = '/'.join(root_dir_lst) + '/'
		output_filename = root_dir + "clean_text"
	return output_filename


if __name__ == '__main__':
	main()
