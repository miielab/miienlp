# Text Cleaning
![Text Cleaning](https://github.com/miielab/TextCleaning/workflows/Text%20Cleaning/badge.svg)


## Description
This platform will perform various cleaning of text for multiple areas of research including but not limited to: lexicon counts, contextual word vectors, sentiment analysis, and bundled constructs. A user can specify which cleaning they want done on their raw text, with some example input files for specific cleaning provided. 



    
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
