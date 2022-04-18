WEAT:

# What does it do?

The purpose of this program is to calculate scores such as association and centeredness between different sets of words to approximate the relationships between those words. Currently, this program can run a group-to-domain test. For example, it can calculate the association between male (group) words with career (domain) words, the association between female (group) words with career (domain) words, and the gender centeredness of the career words.

After running those tests, this program can also clean and visualize the output of those tests.

## WEAT metrics
The metrics specific to the WEAT tests are defined as follows:

Association: mean of all the pairwise cosine similarities between word embeddings from two sets of words. Sometimes referred to as the association/the cosine similarity between two sets of words.

Female or Male Association: If the domain is stated as X, then the female or male association is the association between female or male words and words of the X domain.

Gender Centeredness: female-domain association minus male-domain association. Might also be referred to as gender bias.

EWP: Percentage of WEAT test words that had a valid word embedding vector.

## WEAT modules

The file used for running WEAT analysis and cleaning (to prepare for visualizations) is main.py. There are three modules that WEAT analysis calls: fetchvec, wordtest, and utils. The WEAT cleaning module is: cleaning.

To run visualizations, you can run line_graphs_viz.R (line graphs) and bar_graphs_viz.R (for bar graphs).

### Fetchvec

Fetchvec looks at your input embeddings and extracts only the embeddings that will be needed to run the tests. These extracted embeddings are stored in a TEMP file (the location of the TEMP file is determined by the out_dir you specify in the YAML file - see the YAML file input descriptions for more details).

### Wordtest

Wordtest runs the actual calculations on the embeddings. The test we are currently using is called the T1 test, which measures male-domain and female-domain associations. For example, if the domain is 'science', we will get (1) the association (i.e. cosine similarity) between the word embeddings for male words and the word embeddings for science words, (2) the association between the word embeddings for female words and the word embeddings for science words, (3) the gender centerdness, which is female-science association minus male-science association, (4) the absolute value of the centeredness,  (5) the effective word percentage, which tells you how many of the words you were testing are actually in the data, and (6) statistics, like t-statistic, p-value, n1 (total # of pairwise cosine similarities calculated between group 1 and the domain), and n2 (total # of pairwise cosine similarities calculated between group 2 and the domain).

### Utils

Contains YAML file parsing functionality and includes helpers for loading tests, loading models, and calculating scores (e.g. association between two sets of words) needed in the Wordtest module.

## Cleaning

Cleans up JSON files that were output by WEAT analysis. It converts multiple JSON files into a single CSV file to prepare for visualizations.

### line_graphs_viz.R

Running this will save line graphs of centeredness or cosine similarity over time. You can edit this file to specify which graphs you want (under the headers "Graphs" and "Saving graphs") and the input/output locations  (under the header "Import Data").

### bar_graphs_viz.R

Running this will save bar graphs of centeredness or cosine similarity for each collection of books. You can edit this file to specify which graphs you want (under the headers "Graphs" and "Saving graphs") and the input/output locations (under the header "Import Data").

# How to Run WEAT analysis and/or cleaning

## How to specify whether you want to analyze WEAT or clean WEAT data
	See explanation and example of input.yaml

## What is required to run WEAT analysis?
	1. Tests:
			    Test File Format
				A valid test file should be a .json file in the following structure:
				{"test":{"name":[...]},...,"name":[...]},
				 {"gender":"male":[...],"female":[...]}}
				 where "test" should contain one or two lists for T1 or T2 respectively and "gender" should contain two lists.
				 Rather than directly writing the list of vocabulary into the JSON file, you should write the path to a txt file containing the vocabulary that you want to use.
	2. Word Embedding models:
				vocab: .txt with one word each line
				vectors: .npy numpy array
	3. Libaries:
				Required: Numpy, sklearn, scipy
	4. input.yaml (See the explanation and example of input.yaml)

## What is required to run WEAT cleaning?
	1. CSV input file (See explanation of "clean.csv")

## Where to put inputs?
	See input.yaml to specify the inputs for the WEAT analysis. See input.yaml and clean.csv to specify the inputs for WEAT cleaning.

## How to run WEAT analysis and/or cleaning:
	To run the code directly:
	1. "python main.py"

	To run the code on a slurm system:
	1. sbatch runbrwl.batch

	If you are on Midway:
		1. module load Anaconda3/5.3.0
		2. conda create -n weat
		3. source activate weat
	If you are on your own computer:
		1. conda create -n weat
		2. conda activate weat
	Then:
	1. conda install numpy
	2. conda install sklearn
	3. conda install scipy
	4. conda install statsmodels
	5. conda install pyyaml
	6. conda install gensim
	7. python main.py

	* After finishing WEAT analysis, delete the TEMP folder that was generated. *

# How to Run WEAT visualizations
	Midway modules:
		1. module load R

	Run:
		Rscript line_graphs_viz.R
		Rscript bar_graphs_viz.R


## Example input.yaml file (customized)
```
---
run_analysis: "t"
run_cleaning: ""
model_directory: "/project2/adukia/miie/text_analysis/models/word2vec/bloomer"
output_directory : "/project2/adukia/miie/text_analaysis/models/weat"
output_file : "/project2/adukia/miie/text_analaysis/models/weat/result.json"
test_directory: "/project2/adukia/miie/text_analaysis/models/weat/test_suite/family"
vocabulary_suffix: "npy"
embeddings_suffix: "txt"
reuse_fetchvec: "t"
clean_csv: "src/clean.csv"
clean_out: "by_decade_weat_data.csv"
```

## YAML file input explanations

| Input | YAML entry | Description |
| --- | --- | -- |
| Run Analysis *(optional)* | run_analysis | An input of "t" means you want to run WEAT analysis. |
| Run Cleaning *(optional)* | run_cleaning | An input of "t" means you want to run WEAT cleaning. |
| Model Directory ***(required for analysis)*** | model_directory | Filepath to the directory containing word embedding models |
| Output Directory ***(required for analysis)*** | output_directory | Filepath to where the TEMP folder (which generated test models and a vocabulary file) should be created and saved. |
| Output File ***(required for analysis)*** | output_file | Filepath to where the WEAT results should be saved. The results will be saved as a JSON file. |
| Test Directory ***(required for analysis)*** | test_directory | Filepath to directory containing json files that specify the groups/domain vocabulary to be tested|
| Embeddings Suffix *(optional)* | embeddings_suffix | The suffix of the files containing word embedding vectors, in order to differentiate these files from the vocabulary files. Default is "npy". |
| Vocabulary Suffix *(optional)* | vocabulary_suffix | The suffix of the files containing the vocabulary that correspond to the word embedding vectors. Default is "txt". |
| Reusing models generated by the Fetchvec module *(optional)* | reuse_fetchvec | If you enter "t" in this field, the pre-processing stage will be skipped, so that the models generated from pre-processing previously are reused. Only turn this on if you are running on the same set of tests. Turning it on may speed up the WEAT computations. |
|  Cleaning CSV file ***(required for cleaning)*** | clean_csv | Filepath to where the input cleaning CSV is located (e.g. clean.csv) |
| Cleaning output file ***(required for cleaning)*** | clean_out | Filepath to where the WEAT cleaning should be saved. The results will be saved as a CSV file.

* If you want to run the same WEAT analysis test on a different book collection and output it to the same JSON file, just change model_directory to the folder containing that other book collection (you can change model_directory as often as you want - if you don't change anything else, WEAT will run the same test and save the results to the same JSON output file). If you want to run a completely new WEAT analysis test, make sure you delete the TEMP file that was generated in the output directory.

## Example clean.csv file
```
category	corpus	file
appearance	children	/project2/adukia/miie/text_analysis/weat/results/by_decade/apr29_children_appearance.json
comparison	children 	/project2/adukia/miie/text_analysis/weat/results/by_decade/apr29_children_comparison.json
business	histwords	/project2/adukia/miie/text_analysis/weat/results/histwords/may4_histwords_business.json
```

## clean.csv file input explanation
This CSV file is used as input for WEAT cleaning. It contains 3 columns: category, corpus, and file. File specifies the JSON file output by WEAT analysis that you want to include in the cleaned output. Category specifies the category that the JSON file is in (e.g. if the JSON file was an 'apparel' test, the category could be 'appearance.' Corpus specifies the corpus that was tested in the JSON file (either "children" or "histwords").


## Dependencies
- [numpy](https://numpy.org/)
- [sklearn](https://scikit-learn.org/)
- [scipy](https://www.scipy.org)
