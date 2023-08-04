# Sentiment Analysis with Categorization

## What does it do?

A BERT (Bidirectional Encoder Representation Transformer) fine-tuned for the task of sentiment analysis is used to calculate the sentiment in sentences in children's books. The user can create a list of words that are part of a certain category (for instance: apple, orange, and mango can be part of the fruit category) and this script will track the sentiment in the sentences that contain mentions of words in these categories. In this way, a user could compare the average sentiment towards different categories: say, male and female characters, or different fields of higher education (STEM vs. humanities majors).

## Note: Create a separate virtual environment for sentiment analysis.

Due to package compatibility issues, it is suggested to create a fresh virtual environment and install packages from `miienlp/miienlp/sentimentAnalysis/requirements.txt`. Then, navigate to `miienlp/miienlp/sentimentAnalysis/src/` and run the sentiment analysis pipeline with `python main.py`.

**IMPORTANT** 

For more details, see:
- [example](https://github.com/miielab/miienlp/blob/main/examples/sentimentAnalysis_example.md) 
- [setup instructions for UChicago MiiE Lab RA ONLY](https://github.com/miielab/miienlp/blob/main/documentation/miie_ra_documentation/sentimentAnalysis.md)
- [setup instructions for running sentiment analysis locally](https://github.com/miielab/miienlp/blob/main/documentation/user_documentation/sentimentAnalysis.md)