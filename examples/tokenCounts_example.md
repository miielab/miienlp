# Token Counts
![Token Counts](https://github.com/miielab/TokenCounts/workflows/Token%20Counts/badge.svg)


## Example (NER Only)

```
---
data_dir: ENTER_YOUR_DATA_DIR_PATH

ner:
  method_name: spacy     #currently the only accepted NER method in our pipeline
  spacy_dataset: en_core_web_lg #the NER pipeline used to run NER (can be en_core_web_sm, en_core_web_lg or en_core_web_trf)
  filter_entities: [CARDINAL, DATE, EVENT, FAC, GPE, LANGUAGE, LAW, LOC, MONEY, NORP, ORDINAL, ORG, PERCENT, PERSON, PRODUCT, QUANTITY, TIME, WORK_OF_ART]                     #what types of spacy entities you would like to extract specifically 
  output_dir: ENTER_YOUR_OUTPUT_DIR_PATH #where you would like your results stored
...

```

## Example (Specific Word Counts Only)

```
---
data_dir: ENTER_YOUR_DATA_DIR_PATH

specific_words:
  categorize_file: supplemental_data/Categories # enter path of the folder - this is the path where you store your domain/group related words txt file
  spacy_dataset: en_core_web_sm 
  subcats: [female, male, ...] # this is the name for your txt file. eg, if you have female.txt file in your category folder, then you put "female" here. 
  type: LU #whether you want to count the lower AND uppercase versions of the text (LU), just the lowercase versions (L) or just the uppercase versions (U)
  output_dir: ENTER_YOUR_OUTPUT_DIR_PATH #where you would like your results stored
...
```
**Note:** the [Categories](https://github.com/miielab/Categories) GitHub repository contains all potential specific words we are interested in (for our analysis in particular). One may create new categories, or rely on the already existing categories. 



## Example (Both NER + Specific Word Counts)

```
---
data_dir: ENTER_YOUR_DATA_DIR_PATH

ner:
  method_name: spacy 
  spacy_dataset: en_core_web_lg 
  filter_entities: [PERSON]  # we only want NER to identify PERSON
  output_dir: /path/to/output_dir/

specific_words:
  categorize_file: /path/to/Categories/  # folder path where you store domain/group txt files. 
  spacy_dataset: en_core_web_lg 
  subcats: [female, female_pronouns_combined, female_pronouns_upper, gendered, male, male_pronouns_combined, male_pronouns_lower, male_pronouns_upper, nationalities, old_female, old_male, plural_female, plural_male, red, singular_female, singular_male, white, young_female, young_male]  #the names of domain/group txt files 
  type: LU 
  output_dir: /path/to/output_dir/
...
````

### How to Run

1. Edit and replace the `input.yaml` file in the [Token Counts folder](https://github.com/miielab/miienlp/tree/main/miienlp/token).
2. Run the customized NER pipeline:
    ```
    $ python main.py -i /path/to/input/yaml
    ```
