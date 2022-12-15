# MiiENLP Source Code (v 1.0.0)

Welcome! 

The MiiENLP open source package is a one stop shop for social scientists to use Natural Language Processing (NLP) techniques to analyze texts and derive meaningful results. We created this package with the aim of making NLP and machine-implemented content analysis techniques more accessible to the general users who have zero or limited proficiency with python. We hope these tools will help our you catalyze new research in fields such as social sciences and computational social sciences. The repository contains the source code and examples for using the packages described in the pipeline below: 


![miienlp-pipeline](https://user-images.githubusercontent.com/30983820/207747948-1eb968d8-e46b-4512-8640-308487bf3c01.png)


If you would like to know more about what each method does, please click the link in Table of Contents section or check out the example folders. 

## Getting Started

If you are familiar with Python, please skip this part and go to Table of Contents section. It is worth noting that you should create a new environment in Python Version 3.7. to avoid any package compatibility issues.

If you are completely new to Python, here are some resources to get you started:

1. Download python 
   - We recommend the users to download and install [Anaconda Python distribution](http://www.anaconda.com/products/distribution). 
   
2. Create a new environment 
   - After installing Anaconda, we will create a new python environment inside Anaconda. Please follow the instructions here to create a Python 3.7.x environment. 
   - Then open your terminal, and type :
    ```
    conda info --envs 
    ```
    to find the new environment you just create. You will get a list of envrionment names and their locations. Copy the location of that environment and type 
    ```
    conda activate /Users/xxx/locations/of/your/environment
    ```

## Table of Contents

1. [Optical Character Recognition (OCR)](https://github.com/miielab/miienlp/tree/main/miienlp/ocr)
2. [Data Aggregation](https://github.com/miielab/miienlp/tree/main/miienlp/aggregation)
3. [Text Cleaning](https://github.com/miielab/miienlp/tree/main/miienlp/text_cleaning)
4. [Token Counts and NER](https://github.com/miielab/miienlp/tree/main/miienlp/token)
5. [Co-occurence](https://github.com/miielab/miienlp/tree/main/miienlp/co_occurrence)
6. [Word Embeddings](https://github.com/miielab/miienlp/tree/main/miienlp/embeddings) 
7. [Word Embedding Association Test (WEAT)](https://github.com/miielab/miienlp/tree/main/miienlp/weat)

**Note:** The code was tested on Python ver. 3.7. We recommend the users to create a new environment in Python ver. 3.7. to use our packages. 



[Contact us](https://www.miielab.com/contact)
