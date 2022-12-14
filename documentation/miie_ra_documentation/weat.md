# WEAT
## How to Run (for UChicago MiiE Lab RA ONLY) 

1. Fork or clone the `WEAT` repository OR locate the directory on Midway by typing: 

   `cd /project2/adukia/miie/text_analysis/code/WEAT`
   

2. Load in Python (`module load python`) and download the dependencies in one of two ways:
  
   ```
	 module load Anaconda3/5.3.0
	 conda create -n weat
	 source activate weat
    ```

3. Run the pipeline:
  ```
  $ python main.py -i /path/to/input/yaml
  ```
  
* After finishing WEAT analysis, delete the TEMP folder that was generated. *
