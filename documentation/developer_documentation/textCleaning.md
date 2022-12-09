# Text Cleaning

### Custom and default options:

| Input | Description |
| --- | --- |
| Raw Data Directory ***(required)*** | User filepath to raw text data |
| N-Grams File *(optional)* | The path to a custom newline-delimited text file where each line consists of a desired n-gram (i.e. "Abraham Lincoln") *(default value is "")* |
| Lemmatize *(optional)* | Whether or not to lemmatize individual words *(default value is False)* |
| Stop Words File *(optional)* | The path to a custom newline-delimited text file where each line consists of one stopword (i.e. "and") *(default is the English stopwords list from nltk)* |
| Add Stop Words *(optional)* | Comma-separated list of stop words to be added to custom or default stop words *(default is [])*|
| Remove Stop Words *(optional)* | Comma-separated list of stop words to be removed from existing custom or default stop words *(default is [])*|
| Categorize Domain Directory *(optional)* | Path to either a CSV file where each line consists of a word followed by its desired category (i.e. "girl, female"). The header of this file should be ["Specific_Word", "Category"] **OR** path to a directory of text files named domain.txt and containing words belonging to that category. *(default value is "")*|
| Categorize Domain Subcats *(optional)* | Comma-separated list of domain categories to be included included in provided domain directory. Required if providing category domain directory. *(default value is [])*|
| Categorize Domain Case Sensitive *(optional)* | Whether or not domain categorizations are case-sensitive *(default value is False)*|
| Categorize Famous Directory *(optional)* | Path to a directory of text files named race_gender.txt and containing names of famous people belonging to that category. *(default value is "")*|
| Categorize Famous Subcats *(optional)* | Comma-separated list of famous race gender categories to be included included in provided famous directory. Required if providing category famous directory. *(default value is [])*|
| Categorize Famous Fuzzy *(optional)* | Whether or not to use Levenshtein distance fuzzy matching to determine famous people matching. *(default value is True)*|
| Categorize Famous Fuzzy Threshold *(optional)* | Fuzzy matching threshold between 0-1 for determining a match. *(default value is 0.9)*|
| spaCy NER Dataset *(optional)* | Type of spaCy NER dataset (ie. en_core_web_lg). Required if using famous categorization or gender SSA classifications *(default value is None)*|
| Standardize File *(optional)* | The path to a CSV file where each line consists of a word and its regex variations followed by its desired standardization (i.e. "Martin Luther King(,\s\|\s)(Jr(\.\|)\|Junior), Martin Luther King Junior" *(default value is "")* |
| Gender SSA File *(optional)* | The path to a CSV file where each line consists of a name followed by its most likely gender (i.e. "Lizzy, female"). Note: these classifications are done using a social security dataset (eventually include the link for download). *(default value is "")*|
| Digits *(optional)* | Whether or not to remove digits from text *(default value is False)*|
| Output Directory *(optional)* | Directory path where resulting data is stored *(default is /path/to/raw_data_directory/../clean_text/)*|
| Lowercase Text *(optional)* | Whether or not to lowercase cleaned text *(default is False)*|
| Special Characters Text *(optional)* | Whether or not to remove special characters (punctuation) *(default is False)*|
