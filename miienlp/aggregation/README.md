# DataAggregation
![Data Aggregation](https://github.com/miielab/DataAggregation/workflows/Data%20Aggregation/badge.svg)

## Description
If you are running TextCleaning or OCR on a folder of files, you may get several txt.file as a result. This package will help you aggregate the txt files into on large txt file so that you can feed this single file into TokenCounts or WordEmbedding pipeline. 

1) ```combined_file_path.py``` will generate a metadata CSV file to feed into the data aggregation pipeline. For example, you have a folder of txt files, and you want to aggregate them into one txt file. The first step is to create a metadata CSV file. 

2) Then you run ```$python main.py -i input.yaml``` 

This script combines data in customizable ways based on a metadata CSV file provided by the user. 

The output metadata.csv will look like this: 
 ```
 path
/miienlp/examples/test_data/test_group/example_group-female.txt
/miienlp/examples/test_data/test_group/example_group-male.txt
 ```

You can also create this csv file manually, with one column "path," and txt file paths as rows. 
