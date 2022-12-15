
# Word Embeddings

## Fully-Customized input.yaml Example

Required inputs: A cleaned txt file. Please use our [TextCleaning (word embedding option)](https://github.com/miielab/miienlp/blob/main/examples/text_cleaning.md) to properly clean the txt file and use that as input. 


Below is an example of an input.yaml file that takes advantage of all possible customizations of the pipeline (described in the [word embeddings setup](https://github.com/miielab/miienlp/blob/main/documentation/user_documentation/wordEmbeddings.md) instructions) for a [book excerpt](https://github.com/miielab/miienlp/blob/main/examples/test_data/example_book_excerpt.txt) for which the path was specified in `data_dir`.

```
---
# word embeddings inputs
data_dir: [test_data/example_book_excerpt.txt]

model:
  name: word2vec
  size: 300
  window: 7
  min_count: 50 # number of models you want to generate 
  workers: 5
  sg: 1
  hs: 1
  negative: 0
  epochs: 10

output:
  output_model_dir: test_data/word2vec_output/   # the output will be "model.bin"
  save_vocab_np: True
  save_vocab_txt: True
...
``` 

