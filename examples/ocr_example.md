# Optical Character Recognition (OCR)

**The only required input is the data directory containing images of text (cf. [test_scans](https://github.com/miielab/miienlp/tree/main/examples/test_data/test_scans)).**

## Example of a default input.yaml file

```
---
raw_data_directory: test_data/test_scans 
...
```

The user can specify additional parameters, such as `output_combined` (*filepath for the OCR'd files*) or `ocr_method` (*Tesseract or Google Vision*). For more details, refer to the [Custom and Default Options](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/ocr.md) Section.


## Example input.yaml file with all the features
```
---
raw_data_directory: test_data/test_scans # the path to the raw data directory is the only required input
combination_type: both 
output_combined: test_data/test_scans/output_combined_directory
output_uncombined: test_data/test_scans/output_uncombined_directory/
ocr_method: Google Vision
confidence_threshold: 0.5
image_ordering: underscore_numerical
language: []
project_id: ocr_google_vision
model_id: 1234
remove_cover_ends: True
preprocess_images: True
...
```


## How to Run

1. Edit and replace the `input.yaml` file in the [OCR folder](https://github.com/miielab/miienlp/tree/main/miienlp/ocr/input_yamls).
2. Run the pipeline:
    ```
    $ python src/main.py
    ```




