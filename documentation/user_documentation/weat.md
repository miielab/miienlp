# WEAT Analysis and/or Cleaning

## How to specify whether you want to analyze WEAT or clean WEAT data
	See explanation and example of input.yaml

## What is required to run WEAT analysis?
	1. Tests:
			    Test File Format
				A valid test file should be a .json file in the following structure:
				{"test":{"name":[...]},...,"name":[...]},
				 {"gender":"male":[...],"female":[...]}}
				 where "test" should contain one or two lists for T1 or T2 respectively and "gender" should contain two lists.
				 Rather than directly writing the list of vocabulary into the JSON file, you should write the path to a txt file containing the vocabulary that you want to use.
	2. Word Embedding models:
				vocab: .txt with one word each line
				vectors: .npy numpy array
	3. Libaries:
				Required: Numpy, sklearn, scipy
	4. input.yaml (See the explanation and example of input.yaml)

## What is required to run WEAT cleaning?
	1. CSV input file (See explanation of "clean.csv")

## Where to put inputs?
	See input.yaml to specify the inputs for the WEAT analysis. See input.yaml and clean.csv to specify the inputs for WEAT cleaning.

## How to run WEAT analysis and/or cleaning:
	To run the code directly:
	1. "python main.py"

	To run the code on a slurm system:
	1. sbatch runbrwl.batch

	If you are on Midway:
		1. module load Anaconda3/5.3.0
		2. conda create -n weat
		3. source activate weat
	If you are on your own computer:
		1. conda create -n weat
		2. conda activate weat
	Then:
	1. conda install numpy
	2. conda install sklearn
	3. conda install scipy
	4. conda install statsmodels
	5. conda install pyyaml
	6. conda install gensim
	7. python main.py

	* After finishing WEAT analysis, delete the TEMP folder that was generated. *

## How to Run WEAT visualizations

Midway modules:

	```
	1. module load R
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
