
# Word Embeddings

## Fully-Customized input.yaml Example

Below is an example of an input.yaml file that takes advantage of all possible customizations of the pipeline (described in the [word embeddings setup](https://github.com/miielab/miienlp/blob/main/documentation/user_documentation/wordEmbeddings.md) instructions) for a [book excerpt](https://github.com/miielab/miienlp/blob/main/examples/test_data/example_book_excerpt.txt) for which the path was specified in `data_dir`.

```
---
# word embedding inputs
data_dir: [test_data/example_book_excerpt.txt]

model:
  name: bert
  size: 300
  window: 7
  min_count: 50
  workers: 5
  sg: 1
  hs: 1
  negative: 0
  epochs: 10

output:
  output_model_dir: test_data/word2vec_output/
  save_vocab_np: True
  save_vocab_txt: True
...
``` 

## How to Run

1. Edit and replace the `input.yaml` file in the [embeddings folder](https://github.com/miielab/miienlp/tree/main/miienlp/embeddings/input_yamls).
2. Run the pipeline:
    ```
    $ python src/main.py -i /path/to/input/yaml
    ```
