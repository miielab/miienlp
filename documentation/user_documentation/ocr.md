# Optical Character Recognition (OCR)

## How to Run 

1. Fork or clone the OCR repo 
2. (Optional) Create a virtual or conda environment and activate that environment (this will ensure that any packages you already have downloaded on your personal computer do not conflict with the packages you will be installing for this analysis).
3. Load in Python (`module load python`) and download the dependencies:
    - In the OCR folder, type:
    ```
    $ pip install --user -r requirements.txt
    ```
4. Edit and save `ocr/src/input.yaml` file.
5. To use our OCR method, you have to apply [google vision api credentials](https://cloud.google.com/vision/docs/setup) and download google application credentials. You will get $300 in free credits to run, test, and deploy workloads if you are a new user of Google Cloud. 
6. After obtaining your google api credentials (for example, we have TextAnalysis--8fc4fa534750.json, please put that in your ocr/src folder, and type this in the terminal: 
   ```
   export GOOGLE_APPLICATION_CREDENTIALS=src/TextAnalysis-8fc4fa534750.json
   ```

7. Run the pipeline:
  ```
  $ python src/main.py
  ```

**IMPORTANT:** See [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/ocr.md) for more options.
