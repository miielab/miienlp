# WEAT

## Example input.yaml file (customized)

For example, we'd like to test the associations between Female/Male related words and Appearance related words. We first create a json file, illustrating the paths of the word list. An example of the json file can be found [here](https://github.com/miielab/miienlp/blob/main/examples/test_data/json_weat/appearance.json)  

## Required Inputs: 
1. specify run_analysis: "t" or "", "t" means you'd like to run the weat analysis. 
2. add model_directory: the folder that cotains model.bin (the output we got from wordembedding)
3. add output_directory and output_file (the output will be a json file) 
4. add test_directory: 


For a detailed description of the parameters, refer to [YAML file inputs](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/autoYAML.md) section.
```
---
run_analysis: "t"
model_directory: "miienlp/examples/test_data/" # this folder contain model.bin (the ouput we got from wordEmbedding)
output_directory : "path/to/output_directory"  # specify your output directory 
output_file : "path/to/output_file.json".     # create your output json file 
test_directory: "miienlp/examples/test_data/json_weat" # you can see that in this repo, we have a /appearance.json file in miienlp/examples/test_data/json_weat folder 
vocabulary_suffix: "npy"
embeddings_suffix: "txt"
reuse_fetchvec: "t"

```


For running the same WEAT analysis test on a different folder and saving the output to the same JSON file, change `model_directory` to the folder containing that other files (the model_directory can be changed as often as needed - if nothing else is changed, WEAT will run the same test and save the results to the same JSON output file). To run a completely new WEAT analysis test, make sure to delete the TEMP file that was generated in the output directory.


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

If you would like to convert json file to a csv file, please refer to [this instruction](https://www.geeksforgeeks.org/convert-json-to-csv-in-python/). 


