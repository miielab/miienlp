
# Word Embeddings

## Fully-Customized input.yaml Example
Below is an example of an input.yaml file that takes advantage of all possible customizations of the pipeline (described in the [word embeddings setup](https://github.com/patriChiril/miie_beta/blob/main/documentation/user_documentation/wordEmbeddings.md) instructions).
```
---
# word embedding inputs
data_dir: [/path/to/WordEmbeddings_folder/]

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
  output_model_dir: /path/to/WordEmbeddings_folder/models
  save_vocab_np: True
  save_vocab_txt: True
...
``` 
