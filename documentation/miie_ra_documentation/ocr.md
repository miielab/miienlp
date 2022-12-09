# Optical Character Recognition (OCR)
## How to Run (for UChicago MiiE Lab RA ONLY) 

1. Fork or clone the OCR repository (OR locate directory on Midway by typing `cd /project2/adukia/miie/text_analysis/code/OCR`)
2. (Optional) If you have access to a compute node that has internet access, you can connect to it now. Otherwise, skip this step.
3. Load in Python (`module load python`) and download the dependencies in one of two ways:
    - In the OCR folder, type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - OR Activate the virtual environment (if you have access to the adukia project space on Midway)
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/OCR/OCR/bin/activate
    ```
3. Edit and save the `OCR/src/input.yaml` file. 
4. If using Google Vision, type:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS=src/google_auth_key/TextAnalysis-8fc4fa534750.json
   ```
   **Note:** If you have forked/cloned this repository you need to specify the path to your own google credentials above (to replace ours). (`src/google_auth_key/TextAnalysis-8fc4fa534750.json`)

5. Run the pipeline:
  ```
  $ python src/main.py
  ```
**IMPORTANT:** See [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/ocr.md) for more options.
