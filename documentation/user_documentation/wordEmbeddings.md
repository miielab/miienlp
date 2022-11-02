# WordEmbeddings

## How to Run
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
3. Edit the data_dir parameter in the default input.yaml file (located at `src/input.yaml`) to include the path where your data is located. For example, if your data was located at `/home/Desktop/testing_data`, your input.yaml file should look like:
```
---
# word embedding inputs
data_dir: [/home/Desktop/testing_data.txt]
...
```
5. Run the default pipeline:
  ```
  $ python src/main.py -i /path/to/input/yaml
  ```
**IMPORTANT:** To customize your word vector pipeline (see the [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/wordEmbeddings.md) section for options), edit and save the `src/input.yaml` file, and then rerun step #5. 
