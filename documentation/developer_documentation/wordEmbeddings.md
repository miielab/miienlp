# Word Embeddings
## Parameter Description
There are different "sections" of parameters for this pipeline, only one which is required to have in your yaml file: 
- `data_dir`: contains the input data directory information in a list format. It has to be a txt file. *(required)*
- `model`: contains information on what parameters/hyperparameters you want included in your model setup
- `output`: contains information on where/what you want outputted once your word vector model is created
**Note:** the `data_dir` input can be a list of txt files, list of directories, or a single directory or file.

### model
For more information on this section, see the documentation for [word2vec](https://radimrehurek.com/gensim/models/word2vec.html).
| Input | Description |
| --- | --- |
| name | Default is word2vec. |
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

