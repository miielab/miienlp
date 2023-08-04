# Sentiment Analysis with Categorization

## What does it do?

A BERT (Bidirectional Encoder Representation Transformer) fine-tuned for the task of sentiment analysis is used to calculate the sentiment in sentences in children's books. The user can create a list of words that are part of a certain category (for instance: apple, orange, and mango can be part of the fruit category) and this script will track the sentiment in the sentences that contain mentions of words in these categories. In this way, a user could compare the average sentiment towards different categories: say, male and female characters, or different fields of higher education (STEM vs. humanities majors).

## Special Instructions to Run Sentiment Analysis with Categorization

1. Create a separate virtual environment with Python 3.10 for sentiment analysis.
    ```
    conda create -n <environment_name> python=3.10
    ```
2. Activate the environment.
    ```
    conda activate <environment_name>
    ```
3. Navigate to the `sentimentAnalysis` directory.
    ```
    cd miienlp/miienlp/sentimentAnalysis
    ```
4. Install Rust, a package needed for sentiment analysis. Follow [this website](https://pypi.org/project/tokenizers/) if errors are encountered.
    ```
    curl https://sh.rustup.rs -sSf | sh -s -- -y
    export PATH="$HOME/.cargo/bin:$PATH"
    ```
4. Install all packages from requirements.txt.
    ```
    pip install -r requirements.txt
    ```
5. Change text inputs (if necessary):
    ```
    cd data
    ```
    Inside the `data` directory within `sentimentAnalysis`, either edit the existing text file or create new text files for sentiment analysis. Include sentences within these text files. The sentences must be separated by line such that there is one sentence per line.
6. Run the pipeline:
    ```
    cd ../src
    python main.py
    ```


Create a separate virtual environment for sentiment analysis.

Due to package compatibility issues, it is suggested to create a fresh virtual environment and install packages from `miienlp/miienlp/sentimentAnalysis/requirements.txt`. Then, navigate to `miienlp/miienlp/sentimentAnalysis/src/` and run the sentiment analysis pipeline with `python main.py`.

**IMPORTANT** 

For more details, see:
- [example](https://github.com/miielab/miienlp/blob/main/examples/sentimentAnalysis_example.md) 
- [setup instructions for UChicago MiiE Lab RA ONLY](https://github.com/miielab/miienlp/blob/main/documentation/miie_ra_documentation/sentimentAnalysis.md)
- [setup instructions for running sentiment analysis locally](https://github.com/miielab/miienlp/blob/main/documentation/user_documentation/sentimentAnalysis.md)