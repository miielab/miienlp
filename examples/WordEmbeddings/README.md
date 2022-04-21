# WordEmbeddings

## Setup
1. Fork or clone the WordEmbeddings repo
2. Change directories to the WordEmbedding repository `$ cd WordEmbeddings`
3. Make sure Python3 is installed on your device and download the dependencies in one of two ways:
    - In the WordEmbeddings directory type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - OR Activate the virtual environment in the adukia project space on Midway
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/word_embedding/word_embedding/bin/activate
    ```
3. Edit the data_dir parameter in the default input.yaml file (located at `src/input.yaml`) to include the path where your data is located. For example, if your data was located at `/home/Downloads/testing_data`, your input.yaml file should look like:
```
---
# word embedding inputs
data_dir: [/home/Downloads/testing_data]
...
```
5. Run the default pipeline:
  ```
  $ python src/main.py -i /path/to/input/yaml
  ```
**IMPORTANT:** To customize your word vector pipeline (see below section for options), edit and save the `src/input.yaml` file, and then rerun step #5. 

## Parameter Description
There are different "sections" of parameters for this pipeline, only one which is required to have in your yaml file: 
- `data_dir`: contains the input data directory information in a list format *(required)*
- `model`: contains information on what parameters/hyperparameters you want included in your model setup
- `output`: contains information on where/what you want outputted once your word vector model is created
**Note:** the `data_dir` input can be a list of txt files, list of directories, or a single directory or file.

### model
For more information on this section, please see the documentation for word2vec or BERT
| Input | Description |
| --- | --- |
| name | The type of model you would like to run. Options: word2vec or bert). Default is word2vec. |
| size | Dimensionality of the word vectors. Default is 300. |
| window | Maximum distance between the current and predicted word within a sentence. Default is 5. |
| min_count | The minimum frequency a word must appear in a text in order to be included in the model. Default is 10. |
| workers | Use these many worker threads to train the model (=faster training with multicore machines). Default is 5. |
| sg | Training algorithm: 1 for skip-gram; otherwise CBOW. Default is 1. |
| hs | If 1, hierarchical softmax will be used for model training. If 0, and negative is non-zero, negative sampling will be use. Default is 1. |
| negative | Maximum distance between the current and predicted word within a sentence. Default is 0.|
| epochs | How many iterations of training that should occur. Default is 5. |

### output
| Input | Description |
| --- | --- |
| output_model_dir | The location where you would like your output model information to be saved. Default is the current working directory. |
| save_vocab_np | Whether you want to save a numpy file containing all of the output vectors. Options: True or False. Default is False. |
| save_vocab_txt| Whether you want to save a text file of all the vocab detected in your text. Options: True or False. Default is False.  |


## Fully-Customized input.yaml Example
Below is an example of an input.yaml file that takes advantage of all possible customizations of the pipeline (described above).
```
---
# word embedding inputs
data_dir: [/home/WordEmbeddings/test_data/clean_emb/]

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
  output_model_dir: /home/WordEmbeddings/models
  save_vocab_np: True
  save_vocab_txt: True
...
``` 
