#!/bin/bash

#SBATCH --job-name=token_counts_job
#SBATCH --output=.output/token_%A_%a.out
#SBATCH --error=.error/token_%A_%a.err
#SBATCH --account=pi-adukia
#SBATCH --time=06:00:00
#SBATCH --partition=gpu2
#SBATCH --gres=gpu:1 
#SBATCH --mem=30G

# load in python and dependencies
module load python
source /project2/adukia/miie/text_analysis/dependencies/token_counts/token_counts/bin/activate

python main.py -i $1