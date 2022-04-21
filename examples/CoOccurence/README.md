# Co-occurrence
## What does it do?
[Co-occurrence](https://towardsdatascience.com/simple-word-embedding-for-natural-language-processing-5484eeb05c06) is a simple and interpretable Natural Language Processing tool that looks at how frequently pairs of words co-occur in a set context window. It is a type of frequency-based word embedding that simply creates a count matrix of pairwise words or categories. Rather than looking at relationships between individual words, this part of the pipeline constructs co-occurrence matrices for word categories, in order to compare how frequently different groups and domains appear in the same context.

## How to Run
1. Fork or clone the Co-occurrence repository
2. Change directories to the Co-occurrence repository `$ cd Co-occurrence`
3. Make sure Python3 is installed on your device and download the dependencies in one of two ways:
    - In the Co-occurrence directory type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - OR Activate the virtual environment in the adukia project space on Midway
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/co_occurrence/co_occurrence/bin/activate
    ```
3. Edit the text, domains, and groups parameters in the default input.yaml file (located at `src/input.yaml`) to include the path where your data is located and save the file. For example, your input.yaml file could look like:
```
---
# Co-Occurrence inputs
text: /home/Downloads/testing_file.txt
domains: /home/supplemental_data/Categories/domain
groups: /home/supplemental_data/Categories/group
...
```
5. Run the default pipeline:
  ```
  $ python src/main.py
  ```
**IMPORTANT:** To customize your co-occurrence pipeline (see below section for options), edit and save the `src/input.yaml` file, and then rerun step #5. 


## Default input.yaml file

```
---
text: /path/to/text
domains: /path/to/domain_directory
groups: /path/to/group_directory
...
```
Some possible [groups](https://github.com/miielab/Categories/tree/main/group) and [domains](https://github.com/miielab/Categories/tree/main/domain) for users without pre-determined categories. These are also located on Midway at `/project2/adukia/miie/text_analysis/supplemental_data/Categories/group/` and `/project2/adukia/miie/text_analysis/supplemental_data/Categories/domain/`

## Possible input.yaml file specifications 
```
---
text: /path/to/text
domains: /path/to/domain_directory
groups: /path/to/group_directory
subcats: [male, female, family, appearance, business]
method: context
window: 3
scaled: False
output: /path/to/output_csv
difference: True
...
```


**The data directory containing raw text, domain and group directories are the only required inputs. Custom flag and default options are detailed below.**


| Input | Description |
| --- | --- |
| Text ***(required)*** | User filepath to text data for co-occurrence|
| Domains ***(required)*** | User filepath to directory containing text files of domain word lists|
| Groups ***(required)*** | User filepath to directory containing text files of group word lists|
| Subcategories | List of categories to be included from files within group and domain folders if user does not want to include all categories *(default is [])*|
| Method | Whether to use a context window of a "sentence" or a specified "context" *(default is "sentence")*|
| Window | How many words the context window should be if using specified context *(default is 4)*|
| Scaled | Whether to scale counts in co-occurrence matrix by the total group or domain counts. Possible inputs include False, "group", "domain" *(default is group)*|
| Output | User filepath to desired output CSV storage *(default is ./co_occurrence.csv)*|
| Difference | Whether to find the difference between the two co-occurrence columns *(default is True)*|

## Dependencies
- [pandas](https://pandas.pydata.org/)
- [yaml](https://pyyaml.org/)
- Get more detail: [requirements](https://github.com/adas-7/Co-occurrence/blob/main/requirements.txt)

