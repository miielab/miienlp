#!/bin/sh

#SBATCH --job-name=new_yaml_all
#SBATCH --account=pi-adukia
#SBATCH --mem=15G
#SBATCH --array=1-38
#SBATCH --time=5:00:00
#SBATCH --ntasks-per-node=1  # number of tasks
#SBATCH --cpus-per-task=1    # number of threads per task
#SBATCH --nodes=38
#SBATCH --output=array_%A_%a.out
#SBATCH --error=array_%A_%a.err

# LOAD MODULES
module load python
source /project2/adukia/miie/text_analysis/dependencies/token_counts/token_counts/bin/activate

# DO COMPUTE WORK
echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_IDs
if [[ $SLURM_ARRAY_TASK_ID = 1 ]]; then
    python main.py -i yaml_files/addamsinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 2 ]]; then
    python main.py -i yaml_files/aiylainput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 3 ]]; then
    python main.py -i yaml_files/alexinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 4 ]]; then
    python main.py -i yaml_files/americasinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 5 ]]; then
     python main.py -i yaml_files/geiselinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 6 ]]; then
     python main.py -i yaml_files/arabinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 7 ]]; then
     python main.py -i yaml_files/apainput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 8 ]]; then
     python main.py -i yaml_files/batchelderinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 9 ]]; then
     python main.py -i yaml_files/belpreinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 10 ]]; then
     python main.py -i yaml_files/bloomer_finput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 11 ]]; then
     python main.py -i yaml_files/bloomer_nfinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 12 ]]; then
     python main.py -i yaml_files/caldecottinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 13 ]]; then
     python main.py -i yaml_files/christopherinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 14 ]]; then
     python main.py -i yaml_files/cskinginput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 15 ]]; then
     python main.py -i yaml_files/es_addamsinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 16 ]]; then
     python main.py -i yaml_files/es_alexinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 17 ]]; then
     python main.py -i yaml_files/es_americasinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 18 ]]; then
     python main.py -i yaml_files/es_belpreinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 19 ]]; then
     python main.py -i yaml_files/es_caldecott_iainput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 20 ]]; then
     python main.py -i yaml_files/es_cskinginput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 21 ]]; then
     python main.py -i yaml_files/es_newbery_iainput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 22 ]]; then
     python main.py -i yaml_files/es_nyt_childseriesinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 23 ]]; then
     python main.py -i yaml_files/es_odysseyinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 24 ]]; then
     python main.py -i yaml_files/es_riverainput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 25 ]]; then
     python main.py -i yaml_files/global_societyinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 26 ]]; then
     python main.py -i yaml_files/grayinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 27 ]]; then
     python main.py -i yaml_files/jewishinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 28 ]]; then
     python main.py -i yaml_files/keatsinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 29 ]]; then
     python main.py -i yaml_files/middle_eastinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 30 ]]; then
     python main.py -i yaml_files/moviesinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 31 ]]; then
     python main.py -i yaml_files/newberyinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 32 ]]; then
     python main.py -i yaml_files/nyt_allinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 33 ]]; then
     python main.py -i yaml_files/riverainput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 34 ]]; then
     python main.py -i yaml_files/sainput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 35 ]]; then
     python main.py -i yaml_files/schneiderinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 36 ]]; then
     python main.py -i yaml_files/skipping_stonesinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 37 ]]; then
     python main.py -i yaml_files/stonewallinput.yaml
elif [[ $SLURM_ARRAY_TASK_ID = 38 ]]; then
     python main.py -i yaml_files/woodsoninput.yaml

fi
