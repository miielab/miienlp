# Text Cleaning

The only required input is the `raw_data_directory` (i.e., the folder containing the text data).

## A few notes
1. When only the raw text data directory is provided, the only cleaning performed will be: 
    - removing excess new line characters and white spaces 
    - removing non-ASCII characters
    
2. When removing special characters, we do not remove the character `_`. This is because when using n-grams or some categorizations, we do not want to split up words.

3. For case-sensitive domain categorizations, all words in a given list must be lowercase unless the word should only be categorized if uppercased. 

4. In order to perform domain categorizations, removing special characters is *highly recommended*.


### Example of a default input.yaml file

```
---
raw_data_directory: /path/to/raw_data_dir # only required input
...
```


### Example of a customized pipeline

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

### Clean Counts input.yaml Example
If you want to use the cleaning txt file to feed into TokenCounts package, you have to set your yaml file like this: 


```
---
raw_data_directory: /path/to/input/folder 
output_directory: /path/to/output/folder 
digits: True
lower: False
...
```

### Clean Vectors input.yaml Example
If you want to use the cleaning txt file to feed into WordEmbedding package, you have to set your yaml file like this: 


```
---
raw_data_directory: /project2/adukia/miie/text_analysis/data/gv_raw/
output_directory: /project2/adukia/miie/text_analysis/data/gv_clean_vec/
digits: True
lower: True
special_characters: True
...
```


## How to Run

1. Edit and replace the `input.yaml` file located in the [Text Cleaning folder](https://github.com/miielab/miienlp/tree/main/miienlp/text_cleaning/src). 

2. Run the default pipeline:
```
$ python src/main.py -i /path/to/input/yaml
```
