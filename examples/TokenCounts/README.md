# TokenCounts
![Token Counts](https://github.com/miielab/TokenCounts/workflows/Token%20Counts/badge.svg)

## What does it do?
Part of speech tagging, Named Entity Recognition (NER), and simply counting the frequency of specific words are all useful NLP techniques that allow you to gain insight into what types of names and words are being used in your text. 

## Setup
1. Fork or clone the TokenCounts repo
2. Change directories to the TokenCounts repository `$ cd TokenCounts`
3. If on Midway, load in Python3 (`module load python`), or make sure it is already installed on your personal device
4. (Optional) Create and activate a virtual environment (this will ensure any packages downloaded on your personal device do not conflict with the dependencies needed to run this script)
5. Download the dependencies in one of two ways:
    - In the TokenCounts directory type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - OR Activate the virtual environment in the Adukia project space on Midway
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/token_counts/token_counts/bin/activate
    ```
4. Download the SpaCy pipeline (required for NER): Note, there are a few different [spacy pipelines](https://spacy.io/usage/v3) you can use, feel free to download as many as you would like to experiment with
    - `python -m spacy download en_core_web_lg`
5. (Optional) Connect to a compute node on Midway or your favorite cloud platform
    - `sinteractive --account=pi-adukia --time=02:00:00 --partition=broadwl --mem=10GB`
    - Remember to adjust the time / memory / partition based on how much time, memory, and compute power your job will need
    
## Example (NER Only)
1. To run *just* NER, create an `input.yaml` file in the `src/` and copy the following. Make the necessary edits.
```
---
data_dir: ENTER_YOUR_DATA_DIR_PATH

ner:
  method_name: spacy #currently the only accepted NER method in our pipeline
  spacy_dataset: en_core_web_lg #the NER pipeline used to run NER (can be en_core_web_sm, en_core_web_lg or en_core_web_trf)
  filter_entities: [PERSON] #what types of spacy entities you would like to extract specifically (default 
  output_dir: ENTER_YOUR_OUTPUT_DIR_PATH #where you would like your results stored
...

```
2. Run the NER pipeline with your customizations:
    - `python src/main.py -i /path/to/input/yaml`

## Example (Specific Word Counts Only)
1. To run *just* specific word counts, create an `input.yaml` file in the `src/` and copy the following. Make the necessary edits.
```
---
data_dir: ENTER_YOUR_DATA_DIR_PATH

specific_words:
  categorize_file: supplemental_data/Categories #list of specific words you are interested in
  spacy_dataset: en_core_web_sm #change this if you need a more accurate NER method
  subcats: [female, male, ...] #change this depending on what categories you want incorporated
  type: LU #whether you want to count the lower AND uppercase versions of the text (LU), just the lowercase versions (L) or just the uppercase versions (U)
  output_dir: ENTER_YOUR_OUTPUT_DIR_PATH #where you would like your results stored
...
```
Note: the [Categories](https://github.com/miielab/Categories) GitHub repository contains all potential specific words we are interested in for our analysis in particular. You may create your own categories that are interesting to you, or go off of the categories we already created. 

2. Run the specific words pipeline with your customizations:
    - `python src/main.py -i /path/to/input/yaml`


## Example (Both NER + Specific Word Counts)
1. To run both specific words and NER in one go, simply combine the fields in the specific word count section with the fields in the NER section into one large input.yaml file and then run `python src/main.py -i /path/to/input/yaml`

```
---
data_dir: /project2/adukia/miie/text_analysis/data/gv_raw/ace/

ner:
  method_name: spacy 
  spacy_dataset: en_core_web_lg 
  filter_entities: [PERSON] 
  output_dir: /project2/adukia/miie/text_analysis/results/ner/ace/

specific_words:
  categorize_file: /project2/adukia/miie/text_analysis/supplemental_data/Categories/ 
  spacy_dataset: en_core_web_lg 
  subcats: [female, female_pronouns_combined, female_pronouns_upper, gendered, male, male_pronouns_combined, male_pronouns_lower, male_pronouns_upper, nationalities, old_female, old_male, plural_female, plural_male, red, singular_female, singular_male, white, young_female, young_male] 
  type: LU 
  output_dir: /project2/adukia/miie/text_analysis/results/specific_words/ace/
...
````

# Parameter Description
| NER Input | Description |
| --- | --- |
| data_dir ***(required)*** | User filepath to cleaned text data directory |
| method_name | Currently the only accepted NER method in our pipeline is spacy |
| spacy_dataset | The NER pipeline used to run NER *(can be en_core_web_sm, en_core_web_lg or en_core_web_trf)*|
| filter_entities | NER extracts entity from a text, which can be dates, times, people, etc. Specify the types of spacy entities you would like to extract specifically (i.e. [PERSON])  |
| output_dir ***(required)*** | Where you would like your results stored |

| Specific Word Counts Input | Description |
| --- | --- |
| data_dir ***(required)*** | User filepath to cleaned text data directory |
| categorize_file | List of specific words you are interested in OR alternatively you can put the file path *(/project2/adukia/miie/text_analysis/supplemental_data/Categories/)* |
| spacy_dataset | Change this if you need a more accurate NER method *(can be en_core_web_sm, en_core_web_lg or en_core_web_trf. among them en_core_web_lg is using a slightly more robust method from spacy)* |
| subcats | Subcats are groups/domins you would like to do token counts (i.e. [female, male_lower, appearance, ...]). *change this depending on what categories you want incorporated and refer to this link for subcats: https://github.com/miielab/Categories If there is new words that you would like to track, you should create a new category for them in supplemental_data/Categories/* |
| type | LU or L or U. Whether you want to count the lower AND uppercase versions of the text *(LU)*, just the lowercase versions *(L)* or just the uppercase versions *(U)* |
| output_dir ***(required)*** | Where you would like your results stored |
