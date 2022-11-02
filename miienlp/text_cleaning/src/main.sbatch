#!/bin/bash

#SBATCH --job-name=clean_job
#SBATCH --output=.out/clean_%A_%a.out
#SBATCH --error=.err/clean_%A_%a.err
#SBATCH --time=10:00:00
#SBATCH --partition=broadwl
#SBATCH --nodes=5
#SBATCH --mem=20G

# load in python and dependencies
module load python
source /project2/adukia/miie/text_analysis/dependencies/text_cleaning/text_cleaning/bin/activate

python main.py -i $1
