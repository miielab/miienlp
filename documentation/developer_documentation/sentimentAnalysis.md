# Sentiment Analysis with Categorization

### Custom and default options:

| Input | Description |
| --- | --- |
| Raw Data Directory ***(required)*** | User filepath to raw text data |
| Output Data Directory ***(required)*** | User filepath to output directory
| Category Data Directory ***(required)*** | User filepath to directory with category data in csv format
| Case-sensitive *(optional)* | Whether or not category words and group labels are case-sensitive
| Fuzzy *(optional)* | Whether or not to use Levenshtein distance fuzzy matching to determine whether a word matches a category word
| Fuzzy Threshold *(optional)* | Fuzzy matching threshold between 0-1 for determining a match. *(default value is 0.9)*|