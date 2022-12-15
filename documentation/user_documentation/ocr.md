# Optical Character Recognition (OCR)

## How to Run 

1. Fork or clone the OCR repository. 
2. (Optional) Create a virtual (or conda) environment and activate that environment (this will ensure that any packages you already have downloaded on your personal computer do not conflict with the packages you will be installing for this analysis).
3. Load in Python (`module load python`) and download the dependencies:
    - In the OCR folder, type:
    ```
    $ pip install --user -r requirements.txt
    ```
4. Edit and save `ocr/src/input.yaml` file.
5. To use our OCR method, you have to apply for [Google Vision API credentials](https://cloud.google.com/vision/docs/setup) and download the Google application credentials. You will get $300 in free credits to run, test, and deploy workloads if you are a new user of Google Cloud. (Note: we recommend [this video](https://www.youtube.com/watch?v=wfyDiLMGqDM&list=PL3JVwFmb_BnSLFyVThMfEavAEZYHBpWEd&index=2) in addition to the aforementioned Google instructions.)

A cost-free alternative technology, is [Tesseract](https://github.com/tesseract-ocr/tesseract). While Tesseract's performance does not match that of Google Vision's, it is close.

6. After obtaining your Google API credentials (e.g., MiiE Lab has TextAnalysis--8fc4fa534750.json), put them into your ocr/src folder, and type the following in the terminal: 
   ```
   export GOOGLE_APPLICATION_CREDENTIALS=src/TextAnalysis-8fc4fa534750.json
   ```

7. Run the pipeline:
  ```
  $ python src/main.py
  ```

**IMPORTANT:** See [custom parameters](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/ocr.md) for more options.
