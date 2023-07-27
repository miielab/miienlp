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

## How to Run

1. Edit and replace the `input.yaml` file in the [sentiment analysis](https://github.com/miielab/miienlp/tree/main/miienlp/sentiment_analysis).
2. Run the pipeline:
    ```
    $ python main.py
    ```
