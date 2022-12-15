# DataAggregation
![Data Aggregation](https://github.com/miielab/DataAggregation/workflows/Data%20Aggregation/badge.svg)

## Description
If you are running TextCleaning on a folder of files, you may get several txt.file as a result. This package will help you aggregate the txt files into on large txt file so that you can feed this single file into TokenCounts or WordEmbedding pipeline. 

1) combined_file_path.py will generate a metadata CSV file to feed into the data aggregation pipeline. For example, you have a folder of txt files, and you want to aggregate them into one txt file. The first step is to create a metadata CSV file. 

2) Then you run ```$python main.py -i input.yaml``` 

This script combines data in customizable ways based on a metadata CSV file provided by the user. 

Let's say that we have a collection of books and we want to determine whether stories that have a female protagonist are told in a different way than stories that have male protagonists. We can create a metadata spreadsheet that has information on the gender of the protagonist and the narration style (first person, not first person) of each book in the dataset. It may look something like this:
```
path,narration_style,protagonist_gender
data/book1.txt,1,female
data/book2.txt,1,male
data/book3.txt,1,female
data/book4.txt,0,female
data/book5.txt,0,male
```
Instead of performing an analysis on each book individually to answer our research questions, we can aggregate these books into larger collections which will give us more accurate, representative results. This script will do the aggregation for us based on how we would like your data grouped.

