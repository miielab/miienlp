# Token Counts
## How to Run
1. Fork or clone the TokenCounts repository
2. Change directories to the TokenCounts repository `$ cd TokenCounts`
3. (MiiE Lab RA ONLY) If on Midway, load in Python3 (`module load python`), or make sure it is already installed on your personal device
4. (Optional) Create and activate a virtual environment (this will ensure any packages downloaded on your personal device do not conflict with the dependencies needed to run this script)
5. Download the dependencies in one of two ways:
    - In the TokenCounts directory type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - (MiiE Lab RA ONLY) OR Activate the virtual environment in the Adukia project space on Midway
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/token_counts/token_counts/bin/activate
    ```
4. Download the SpaCy pipeline (required for NER): Note, there are a few different [spacy pipelines](https://spacy.io/usage/v3) you can use, feel free to download as many as you would like to experiment with
    - `python -m spacy download en_core_web_lg`
5. (Optional) Connect to a compute node on Midway or your favorite cloud platform
    - `sinteractive --account=pi-adukia --time=02:00:00 --partition=broadwl --mem=10GB`
    - Remember to adjust the time / memory / partition based on how much time, memory, and compute power your job will need

**IMPORTANT:** For more details, see the [Parameter Description](https://github.com/patriChiril/miie_beta/blob/main/documentation/developer_documentation/tokenCounts.md) section.
