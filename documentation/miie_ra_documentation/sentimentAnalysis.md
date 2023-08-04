# Sentiment Analysis with Categorization

## How to Run (for UChicago MiiE Lab RA ONLY) 

1. Go to the sentimentAnalysisCategorization folder on Midway:
```
$ cd /project2/adukia/miie/text_analysis/code/SentimentAnalysisCategorization/sentimentAnalysis
```
2. (Optional) connect to a compute node on Midway.
3. Load in Python (`module load python`) and the activate virtual environment:
```
$ module load python
$ source /project2/adukia/miie/text_analysis/dependencies/sentiment_analysis_categorization/sentiment_analysis_categorization_venv/bin/activate
```
4. Enter the src directory
```
$ cd src
```
4. Run the pipeline:
```
$ python3 main.py -i /path/to/input/yaml
```