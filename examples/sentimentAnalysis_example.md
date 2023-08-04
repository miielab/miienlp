# Sentiment Analysis with Categorization

## Example (with fuzzy categorization)

```
---
data_dir: # enter path to data directory
category_dir: # enter path to directory with categories.csv file
output_dir: # enter path to output directory
case_sensitive: True
fuzzy: True
threshold_fuzzy: 0.9
...

```

## Example (without fuzzy categorization)
```
---
data_dir: # enter path to data directory
category_dir: # enter path to directory with categories.csv file
output_dir: # enter path to output directory
case_sensitive: True
fuzzy: False
threshold_fuzzy: 0
...

```

## Example of input text file
```
I am feeling okay today.
I am happy today!
I am very disappointed.
```

Each of the sentences need to be separated by line (one sentence per line). This file can be found in the `data` directory of the `sentimentAnalysis` folder.

## How to Run

1. Edit and replace the `input.yaml` file in the [sentiment analysis](https://github.com/miielab/miienlp/tree/main/miienlp/sentiment_analysis).
2. Note: the input data is in the `sentimentAnalysis/data/` directory while the output directory is in `sentimentAnalysis/output`.
3. Navigate to the `src` directory and run the pipeline:
    ```
    $ cd src
    $ python main.py
    ```
