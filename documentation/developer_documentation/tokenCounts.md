# Token Counts
## Parameter Description
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
