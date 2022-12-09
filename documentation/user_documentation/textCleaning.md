# Text Cleaning

## How to Run 

1. Fork or clone the `TextCleaning` repository. 
2. (Optional) Create a virtual (or conda) environment and activate that environment (this will ensure that any packages you already have downloaded on your personal computer do not conflict with the packages you will be installing for this analysis).
3. Load in Python (`module load python`) and download the dependencies:
    - In the TextCleaning folder, type:
    ```
    $ pip install --user -r requirements.txt
    ```
4. Edit and save `ocr/src/input.yaml` file.
  
5. Run the pipeline:
  ```
  $ python src/main.py -i /path/to/input/yaml
  ```
  
  
  

**IMPORTANT:** See [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/textCleaning.md) for more options.
