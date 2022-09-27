# WEAT

## Example input.yaml file (customized)
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
clean_csv: "path/to/clean.csv"
clean_out: "file_name.csv"
```



* If you want to run the same WEAT analysis test on a different book collection and output it to the same JSON file, just change model_directory to the folder containing that other book collection (you can change model_directory as often as you want - if you don't change anything else, WEAT will run the same test and save the results to the same JSON output file). If you want to run a completely new WEAT analysis test, make sure you delete the TEMP file that was generated in the output directory.

## Example clean.csv file
```
category	corpus	  file
appearance	children	weat/results/children_appearance.json
comparison	children 	weat/results/children_comparison.json
business	histwords	weat/results/histwords_business.json
```

## clean.csv file input explanation
This CSV file is used as input for WEAT cleaning. It contains 3 columns: category, corpus, and file. File specifies the JSON file output by WEAT analysis that you want to include in the cleaned output. Category specifies the category that the JSON file is in (e.g. if the JSON file was an 'apparel' test, the category could be 'appearance.' Corpus specifies the corpus that was tested in the JSON file (either 'children' or 'histwords').
