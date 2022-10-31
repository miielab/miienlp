#!/bin/bash

#SBATCH --job-name=word_vectors
#SBATCH --output=.out/vectors_%A_%a.out
#SBATCH --error=.err/vectors_%A_%a.err
#SBATCH --account=pi-adukia
#SBATCH --time=36:00:00
#SBATCH --partition=broadwl
#SBATCH --nodes=3
#SBATCH --mem=10G

# load in python and dependencies
echo "Job started at `date`"
echo using $1 as input
module load python
source /project2/adukia/miie/text_analysis/dependencies/word_embedding/word_embedding/bin/activate


python main.py -i $1
echo "Job finished at `date`"
