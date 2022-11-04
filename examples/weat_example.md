# WEAT

## Example input.yaml file (customized)

For a detailed description of the parameters, refer to [YAML file inputs](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/autoYAML.md) section.
```
---
run_analysis: "t"
run_cleaning: ""
model_directory: "path/to/model_directory"
output_directory : "path/to/output_directory"
output_file : "path/to/output_file.json"
test_directory: "path/to/test_directory"
vocabulary_suffix: "npy"
embeddings_suffix: "txt"
reuse_fetchvec: "t"
clean_csv: "test_data/clean.csv"
clean_out: "file_name.csv"
```


For running the same WEAT analysis test on a different book collection and saving the output to the same JSON file, change `model_directory` to the folder containing that other book collection (the model_directory can be changed as often as needed - if nothing else is changed, WEAT will run the same test and save the results to the same JSON output file). To run a completely new WEAT analysis test, make sure to delete the TEMP file that was generated in the output directory.


## [clean.csv](https://github.com/miielab/miienlp/blob/main/examples/test_data/clean.csv) file input explanation
This CSV file is used as input for WEAT cleaning. It contains 3 columns: category, corpus, and file. 
* File specifies the JSON file output by WEAT analysis that you want to include in the cleaned output. 
* Category specifies the category that the JSON file is in (e.g., if the JSON file was an *'apparel'* test, the category could be *'appearance'*. 
* Corpus specifies the corpus that was tested in the JSON file (either *'children'* or *'histwords'*).

## How to Run

1. Edit and replace the `input.yaml` file in the [weat folder](https://github.com/miielab/miienlp/tree/main/miienlp/weat).
2. [Run the pipeline](https://github.com/miielab/miienlp/blob/main/documentation/user_documentation/weat.md).

## Output Explaination 
The output will be stored as a json file. It may look like this: 

'''
{
            "appearance": {
                        "model": {
                                    "M_Assoc": 0.7939108979019815,
                                    "F_Assoc": 0.9106496851984686,
                                    "Abs_Bias": 0.11673878729648701,
                                    "Bias": 0.11673878729648701,
                                    "EWP": 0.2,
                                    "P_value": 0.7669462792247821,
                                    "T_statistic": -0.29637164228572616,
                                    "N1": 3.0,
                                    "N2": 2.0
                        }
            }
}
''' 

Since we calculate the cosin-similarity betweens male/female words and apperance-related words, the results here mean that appearance words are more associated with female than male. The range for association is from 0 to 1. 0 means that are not related. 



