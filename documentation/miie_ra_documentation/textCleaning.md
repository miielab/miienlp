# Text Cleaning
## How to Run (for UChicago MiiE Lab RA ONLY) 

1. Fork or clone the `TextCleaning` repository OR locate directory on Midway by typing:
 
`cd /project2/adukia/miie/text_analysis/code/TextCleaning`
3. (Optional) If you have access to a compute node that has internet access, you can connect to it now. Otherwise, skip this step.
4. Load in Python (`module load python`) and download the dependencies in one of two ways:
    - In the TextCleaning folder, type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - OR Activate the virtual environment if you have access to the adukia project space on Midway
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/text_cleaning/text_cleaning/bin/activate
    ```
    
4. Run the pipeline:
  ```
  $ python src/main.py -i /path/to/input/yaml
  ```
  
 **IMPORTANT:** See [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/textCleaning.md) for more options.


