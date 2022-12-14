# WEAT Analysis and/or Cleaning

## What is required to run WEAT analysis?

`1. Test File Format:`

A valid test file should be a .json file with the following structure:
  ```
{"test":{"name":[...]},...,"name":[...]},
{"gender":"male":[...],"female":[...]}}
  ```
where *'test'* should contain one or two lists for T1 or T2 respectively and *'gender'* should contain two lists. Rather than directly writing the list of vocabulary into the JSON file, one should write the path to a txt file containing the vocabulary that needs to be used.

`2. Word Embedding models:`
* vocab: .txt with one word per line
* vectors: .npy numpy array

`3. Libaries required:` Numpy, sklearn, scipy

`4. input.yaml` 



## How to run WEAT analysis 

To run the code:
  ```
  1. conda create -n weat
  2. conda activate weat
  3. conda install numpy
  4. conda install -c anaconda scikit-learn
  5. conda install scipy
  6. conda install statsmodels
  7. conda install pyyaml
  8. conda install gensim
  
  "python main.py"
  ```
 	
  

**After finalizing the WEAT analysis, delete the TEMP folder that was generated.**


