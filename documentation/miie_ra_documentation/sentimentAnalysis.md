# Sentiment Analysis with Categorization

## How to Run (for UChicago MiiE Lab RA ONLY) 

1. Go to the sentimentAnalysisCategorization folder on Midway:
```
$ cd /project2/adukia/miie/text_analysis/code/sentimentAnalysisCategorization
```
2. (Optional) connect to a compute node on Midway.
3. Load in Python (`module load python`) and the activate virtual environment:
```
$ module load python
$ source /project2/adukia/miie/text_analysis/dependencies/sentiment_analysis_categorization/sentiment_analysis_categorization_venv/bin/activate
```
4. Run the pipeline:
```
$ python3 src/main.py -i /path/to/input/yaml
```