# Text Cleaning
![Text Cleaning](https://github.com/miielab/TextCleaning/workflows/Text%20Cleaning/badge.svg)


## Description
This platform will perform various cleaning of text for multiple areas of research including but not limited to: lexicon counts, contextual word vectors, sentiment analysis, and bundled constructs. A user can specify which cleaning they want done on their raw text, with some example input files for specific cleaning provided. 


## Setup 
1. Fork or clone the TextCleaning repo and change directories (`cd TextCleaning`)
2. (Optional) Connect to a compute node (if on Midway)
3. Install Python (or type `module load python` on Midway)
4. (Optional) Create a virtual or conda environment (will ensure packages installed on your device will not conflict with the ones needed for this analysis)
5. Download the dependencies in one of two ways:
    - In the `TextCleaning` folder type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - OR Activate the virtual environment in the adukia project space on Midway
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/text_cleaning/text_cleaning/bin/activate
    ```
    
## Example (default pipeline)
1. Edit or create an input.yaml file located at src/input.yaml. Add your raw_data_directory path (i.e. where your data is located) and save the file. Your yaml file should look something like this: 
```
---
raw_data_directory: /path/to/raw_data_dir # only required input
...
```
2. Run the default pipeline:
```
$ python src/main.py -i /path/to/input/yaml
```

## Example (customized pipeline)
1. To customize your text cleaning pipeline (see below table for options), edit and save the `src/input.yaml` file and run the pipeline (`python src/main.py -i /path/to/input/yaml`)

### Customizable input.yaml file specifications 
```
---
raw_data_directory: /path/to/raw_data_dir
n_gram_file: /path/to/ngram_file
lemmatize: False
stopwords_file: /path/to/stopwords_file
stopwords_add: [she, her]
stopwords_remove: [the]
categorize_domain:
  directory: /path/to/domain_categorizations_directory
  subcats: [domain1, domain2, domain3]
  case_sensitive: False
categorize_famous:
  directory: /path/to/famous_categorizations_directory
  subcats: [famous1, famous2, famous3]
  fuzzy: True
  threshold_fuzzy: 0.9
spacy_ner_dataset: en_core_web_lg
standardize_file: /path/to/standardize_file
gender_ssa_file: /path/to/gender_ssa_file
digits: True
output_directory: /path/to/output_directory
lower: False
special_characters: False
...
```

**The data directory containing raw text is the only required input. Custom flag and default options are detailed below.**

| Input | Description |
| --- | --- |
| Raw Data Directory ***(required)*** | User filepath to raw text data |
| N-Grams File *(optional)* | The path to a custom newline-delimited text file where each line consists of a desired n-gram (i.e. "Abraham Lincoln") *(default value is "")* |
| Lemmatize *(optional)* | Whether or not to lemmatize individual words *(default value is False)* |
| Stop Words File *(optional)* | The path to a custom newline-delimited text file where each line consists of one stopword (i.e. "and") *(default is the English stopwords list from nltk)* |
| Add Stop Words *(optional)* | Comma-separated list of stop words to be added to custom or default stop words *(default is [])*|
| Remove Stop Words *(optional)* | Comma-separated list of stop words to be removed from existing custom or default stop words *(default is [])*|
| Categorize Domain Directory *(optional)* | Path to either a CSV file where each line consists of a word followed by its desired category (i.e. "girl, female"). The header of this file should be ["Specific_Word", "Category"] **OR** path to a directory of text files named domain.txt and containing words belonging to that category. *(default value is "")*|
| Categorize Domain Subcats *(optional)* | Comma-separated list of domain categories to be included included in provided domain directory. Required if providing category domain directory. *(default value is [])*|
| Categorize Domain Case Sensitive *(optional)* | Whether or not domain categorizations are case-sensitive *(default value is False)*|
| Categorize Famous Directory *(optional)* | Path to a directory of text files named race_gender.txt and containing names of famous people belonging to that category. *(default value is "")*|
| Categorize Famous Subcats *(optional)* | Comma-separated list of famous race gender categories to be included included in provided famous directory. Required if providing category famous directory. *(default value is [])*|
| Categorize Famous Fuzzy *(optional)* | Whether or not to use Levenshtein distance fuzzy matching to determine famous people matching. *(default value is True)*|
| Categorize Famous Fuzzy Threshold *(optional)* | Fuzzy matching threshold between 0-1 for determining a match. *(default value is 0.9)*|
| spaCy NER Dataset *(optional)* | Type of spaCy NER dataset (ie. en_core_web_lg). Required if using famous categorization or gender SSA classifications *(default value is None)*|
| Standardize File *(optional)* | The path to a CSV file where each line consists of a word and its regex variations followed by its desired standardization (i.e. "Martin Luther King(,\s\|\s)(Jr(\.\|)\|Junior), Martin Luther King Junior" *(default value is "")* |
| Gender SSA File *(optional)* | The path to a CSV file where each line consists of a name followed by its most likely gender (i.e. "Lizzy, female"). Note: these classifications are done using a social security dataset (eventually include the link for download). *(default value is "")*|
| Digits *(optional)* | Whether or not to remove digits from text *(default value is False)*|
| Output Directory *(optional)* | Directory path where resulting data is stored *(default is /path/to/raw_data_directory/../clean_text/)*|
| Lowercase Text *(optional)* | Whether or not to lowercase cleaned text *(default is False)*|
| Special Characters Text *(optional)* | Whether or not to remove special characters (punctuation) *(default is False)*|

## Dependencies
- [pandas](https://pandas.pydata.org/)
- [nltk](https://www.nltk.org/)
- [spaCy](https://spacy.io/)

Please see the [requirements.txt](https://github.com/miielab/text_analysis/blob/main/requirements.txt) file for details on versions and other requirements


## A few notes
- When only the raw text data directory is provided, the only cleaning performed will be (1) removing excess new line characters and white spaces and (2) removing non-ASCII characters
- When removing special characters, we do not remove the character `_`. This is because when using n-grams or some categorizations, we do not want to split up words.
- For case-sensitive domain categorizations, all words in a given list must be lowercase unless the word should only be categorized if uppercased. 
- In order to perform domain categorizations, removing special characters is *highly recommended*


## Clean Counts input.yaml Example

```
---
raw_data_directory: /project2/adukia/miie/text_analysis/data/gv_raw/
output_directory: /project2/adukia/miie/text_analysis/data/gv_clean_counts/
digits: True
lower: False
...
```

## Clean Vectors input.yaml Example

```
---
raw_data_directory: /project2/adukia/miie/text_analysis/data/gv_raw/
output_directory: /project2/adukia/miie/text_analysis/data/gv_clean_vec/
digits: True
lower: True
special_characters: True
...
```

## Race Gender Bundled Constructs input.yaml Example

```
---
raw_data_directory: /project2/adukia/miie/text_analysis/data/gv_raw/
output_directory: /project2/adukia/miie/text_analysis/data/clean_bundled_constructs/
digits: True
lower: True
special_characters: True
categorize_domain:
  directory: /project2/adukia/miie/text_analysis/supplemental_data/Categories
  subcats: [business, education, entertainment, power, sports, struggle, wealth, tools, occupations]
  case_sensitive: True
categorize_famous:
  directory: /project2/adukia/miie/text_analysis/supplemental_data/Categories/group
  subcats: [white_male, black_male, white_female, black_female]
  fuzzy: True
  threshold_fuzzy: 0.9
spacy_ner_dataset: en_core_web_lg
gender_ssa_file: /project2/adukia/miie/visualizations/supplemental/data/SSA_names.csv
...
```
