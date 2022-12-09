# WordEmbeddings

## How to Run 

1. Fork or clone the `WordEmbeddings` repository OR locate directory on Midway by typing
   `cd /project2/adukia/miie/text_analysis/code/WordEmbeddings`)
2. (Optional) If you have access to a compute node that has internet access, you can connect to it now. Otherwise, skip this step.
3. Load in Python (`module load python`) and download the dependencies in one of two ways:
    - In the WordEmbeddings folder, type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - OR Activate the virtual environment (if you have access to the adukia project space on Midway)
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/word_embedding/word_embedding/bin/activate

4. Edit the `data_dir` parameter in the default input.yaml file (located at `src/input.yaml`) to include the path where your data is located. 

5. Run the default pipeline:
  ```
  $ python src/main.py -i /path/to/input/yaml
  ```
**IMPORTANT:** See [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/wordEmbeddings.md) for more options.
