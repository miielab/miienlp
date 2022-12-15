# WordEmbeddings

## How to Run

Required inputs: A cleaned txt file. Please use our [TextCleaning (word embedding option)](https://github.com/miielab/miienlp/blob/main/examples/text_cleaning.md) to properly clean the txt file and use that as input. 


1. Fork or clone the `WordEmbeddings` repository.
2. (Optional) Create a virtual (or conda) environment and activate that environment (this will ensure that any packages you already have downloaded on your personal computer do not conflict with the packages you will be installing for this analysis).
3. Load in Python (`module load python`) and download the dependencies:
    - In the WordEmbeddings directory type:
    ```
    $ pip install --user -r requirements.txt
    ```
   
4. Edit the data_dir parameter in the default input.yaml file (located at `src/input.yaml`) to include the path where your data is located. 

5. Run the default pipeline:
  ```
  $ python src/main.py -i /path/to/input/yaml
  ```
**IMPORTANT:** See [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/wordEmbeddings.md) for more options.
