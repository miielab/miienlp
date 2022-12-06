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

## What is required to run WEAT cleaning?
`CSV input file` (See the [example](https://github.com/miielab/miienlp/blob/main/examples/weat_example.md)).


## How to run WEAT analysis and/or cleaning:

To run the code directly:
  ```
  "python main.py"
  ```
  
To run the code on a slurm system (MiiE Lab RA ONLY):
  ```	
  sbatch runbrwl.batch
  ```
  
If you are on Midway (MiiE Lab RA ONLY):
  ```
  1. module load Anaconda3/5.3.0
  2. conda create -n weat
  3. source activate weat
  ```	
  
If you are on your own computer:
  ```
  1. conda create -n weat
  2. conda activate weat
  ```
  
Then:
  ```
  1. conda install numpy
  2. conda install sklearn
  3. conda install scipy
  4. conda install statsmodels
  5. conda install pyyaml
  6. conda install gensim
  7. python main.py
  ```

**After finalizing the WEAT analysis, delete the TEMP folder that was generated.**

## How to Run WEAT visualizations

Midway modules:
  ```
  module load R
  ```  

Run:
  ```
  Rscript line_graphs_viz.R
  Rscript bar_graphs_viz.R
  ```	

## Dependencies
- [numpy](https://numpy.org/)
- [sklearn](https://scikit-learn.org/)
- [scipy](https://www.scipy.org)

**IMPORTANT:** For more details regarding the modules, see the [details](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/weat.md) section.
