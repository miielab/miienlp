# Token Counts
## How to Run (for UChicago MiiE Lab RA ONLY) 

1. Fork or clone the `TokenCounts` repository OR locate the directory on Midway by typing: 

   `cd /project2/adukia/miie/text_analysis/code/TokenCounts`
   
2. (Optional) If you have access to a compute node that has internet access, you can connect to it now. Otherwise, skip this step.
3. Load in Python (`module load python`) and download the dependencies in one of two ways:
    - In the TokenCounts folder, type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - OR Activate the virtual environment (if you have access to the adukia project space on Midway)
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/token_counts/token_counts/bin/activate
    ```
4. Download the SpaCy pipeline (required for NER): Note, there are a few different [spacy pipelines](https://spacy.io/usage/v3) you can use, feel free to download as many as you would like to experiment with
    - `python -m spacy download en_core_web_lg`

5. (Optional) Connect to a compute node on Midway or your favorite cloud platform
    - `sinteractive --account=pi-adukia --time=02:00:00 --partition=broadwl --mem=10GB`
    - Remember to adjust the time / memory / partition based on how much time, memory, and compute power your job will need
 
6. Run the pipeline:
  ```
  $ python src/main.py -i /path/to/input/yaml
  ```
**IMPORTANT:** See [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/tokenCounts.md) for more options.

**Note:** We have compiled a list of domain and group related words for users to use: the [Categories](https://github.com/miielab/Categories) GitHub repository contains all potential specific words we are interested in (for our analysis in particular). One may create new categories, or rely on the already existing categories. 
