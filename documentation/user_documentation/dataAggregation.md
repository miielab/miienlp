# Data Aggregation
## How to Run
### For people with Midway access:
1. Go to the DataAggregation folder on Midway and git pull to make sure you have the most updated version of the script:
```
$ cd /project2/adukia/miie/text_analysis/code/DataAggregation
$ git pull
```
2. (Optional) connect to a compute node on Midway
3. Load in Python (`module load python`) and the activate virtual environment:
```
$ module load python
$ source /project2/adukia/miie/text_analysis/dependencies/data_aggregation/data_aggregation/bin/activate
```
### For people running this script on their personal device:
1. Clone or fork the DataAggregation repository on your personal device and then change into the DataAggregation directory:
```
$ git clone https://github.com/miielab/DataAggregation.git
$ cd DataAggregation
```
2. (Optional) Create a virtual or conda environment and activate that environment (this will ensure that any packages you already have downloaded on your personal computer do not conflict with the packages you will be installing for this analysis).

3. Load in the dependencies (provided you have Python3 and pip installed on your device):
```
$ pip install -r requirements.txt
```
