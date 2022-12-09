# Token Counts
## How to Run
1. Fork or clone the `TokenCounts` repository.
2. (Optional) Create and activate a virtual environment (this will ensure any packages downloaded on your personal device do not conflict with the dependencies needed to run this script)
3. Load in Python (`module load python`) and download the dependencies:
    - In the TokenCounts directory type:
    ```
    $ pip install --user -r requirements.txt
    ```

4. Download the SpaCy pipeline (required for NER): Note, there are a few different [spacy pipelines](https://spacy.io/usage/v3) you can use, feel free to download as many as you would like to experiment with:
    - `python -m spacy download en_core_web_lg`

5. Run the pipeline:
  ```
  $ python src/main.py -i /path/to/input/yaml
  ```
**IMPORTANT:** See [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/tokenCounts.md) for more options.

