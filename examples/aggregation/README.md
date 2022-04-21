# DataAggregation
![Data Aggregation](https://github.com/miielab/DataAggregation/workflows/Data%20Aggregation/badge.svg)

## Description
This script combines your data in customizable ways based on a metadata CSV file provided by the user. 

Let's say for example you have a collection of books and you want to determine whether stories that have a female protagonist are told in a different way than stories that have male protagonists. You can create a metadata spreadsheet that has information on the gender of the protagonist and the narration style (first person, not first person) of each book in your dataset. It may look something like this:
```
path,narration_style,protagonist_gender
/project2/adukia/miie/text_analysis/data/gv_clean_counts/americas/2000/2005_americas_commended_carlson.txt,1,female
/project2/adukia/miie/text_analysis/data/gv_clean_counts/arab/2000/2007_arab_winner_khalidi.txt,1,male
/project2/adukia/miie/text_analysis/data/gv_clean_counts/bloomer_nf/2010/2014_bloomer_nf_winner_abdi.txt,1,female
/project2/adukia/miie/text_analysis/data/gv_clean_counts/newbery_ia/1940/1947_newbery_honor_barnes.txt,0,female
/project2/adukia/miie/text_analysis/data/gv_clean_counts/americas/1990/1995_americas_winner_temple.txt,0,male
```
Instead of running analysis on each book individually to answer your research question, you can aggregate these books into larger collections which will give you more accurate, representative results. This script will do the aggregation for you based on how you would like your data grouped.

Hello!

## Setup
### For people with Midway access:
1. Go to the DataAggregation folder on Midway and git pull to make sure you have the most updated version of the script:
```
$ cd /project2/adukia/miie/text_analysis/code/DataAggregation
$ git pull
```
2. (Optional) connect to a compute node on Midway
3. Load in Python (`module load python`) and the activate virtual environment:
```
$ module load python
$ source /project2/adukia/miie/text_analysis/dependencies/data_aggregation/data_aggregation/bin/activate
```
### For people running this script on their personal device:
1. Clone or fork the DataAggregation repository on your personal device and then change into the DataAggregation directory:
```
$ git clone https://github.com/miielab/DataAggregation.git
$ cd DataAggregation
```
2. (Optional) Create a virtual or conda environment and activate that environment (this will ensure that any packages you already have downloaded on your personal computer do not conflict with the packages you will be installing for this analysis).

3. Load in the dependencies (provided you have Python3 and pip installed on your device):
```
$ pip install -r requirements.txt
```

## Example

To run data aggregation first create an input.yaml (`vim input.yaml`) file with the following required fields:
1. `metadata_file`: **(required)** this is the path to your metadata file containing all of the data (filepaths) you want considered in your run
2. `groups`: (optional) list of lists OR dictionary which describe how you want to group your data
3. `output_dir`: (optional) where you want your grouped data stored

Example input.yaml file (list of lists):
```
metadata_file: test_suite/metadata_protagonist.csv
groups: [[protagonist_gender, narration_style], [protagonist_gender]]
output_dir: test_suite/combined/
```
The metadata_protagonist CSV file under `metadata_file` records a narrator's gender and narration style for a small set of books. 
The `groups` variable specifies what metrics you would like your dataset combined by, in this case we want to group our data by protagonist_gender and narration_style AND by protagonist_gender itself. If you would only like to group in one way, you would still keep the list of list format: \[\[protagonist_gender\]\]. The `groups` variables MUST match the name of a column in your `metadata_file`. The `output_dir` is the directory path where your resulting aggregated files will all be saved. 

Example input.yaml file (dictionary):
```
metadata_file: test_suite/metadata_protagonist.csv
groups: 
  gender_narration: [protagonist_gender, narration_style]
  gender: [protagonist_gender]
output_dir: test_suite/combined/
```
This input.yaml file contains the same fields as above but the `groups` is organized in a dictionary. This is another way you can structure your input.yaml file that will allow you to customize how your final aggregated files are organized in the `output_dir` folder. For example, the aggregated files will be stored in the output_dir file as `test_suite/combined/gender_narration/` and `test_suite/combined/gender/`, where `gender_narration` and `gender` are the keys in the dictionary under `groups`. This is an optional way to keep things more organized. 

To aggregate your data, run the following (from the `DataAggregation` folder):
```
$ python src/main.py -i /path/to/input.yaml
```
The combined datasets will be stored under the output_dir filepath specified in the input.yaml file. If the output_dir parameter is not specified in the input.yaml file, the script will store the results in a folder named `combined/` in the user's current working directory. 

Inside `combined/` for the above list of lists input.yaml file, you should see 6 text files. `female_0.txt` corresponds to all female protagonist books that are NOT first-person narratives, `female_1.txt` corresponds to all female protagonist books that are first-person narratives, and `female.txt` corresponds to all female protagonist books. Same idea for male protagonist books.


## Dependencies
- pandas
- numpy
For more information on versions and other dependencies, see the requirements.txt file
