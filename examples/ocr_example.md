# Optical Character Recognition (OCR)

** Required Inputs: **
1. raw_data_directory: A directory containing images of text (cf. [test_scans](https://github.com/miielab/miienlp/tree/main/examples/test_data/test_scans)).
2. write the output path for output_combined, and output_uncombined parameters. 

## Example of a default input.yaml file

```
---
#OCR inputs
 # REQUIRED: path to directory containing image files. 
raw_data_directory: /miienlp/examples/test_data/test_scans/ 
combination_type: both
output_combined: /miienlp/examples/test_data/test_scans/combined   
output_uncombined: /miienlp/examples/test_data/test_scans/uncombined
ocr_method: Google Vision 
confidence_threshold: 0.5 # Value between 0 and 1, inclusive
image_ordering: alphabetical # order: page_1.jpg, page_2.jpg, page_3.jpg
language: ["English"]
project_id: facedetectioncartoons  # google vision project id
model_id: # google vision model ID
remove_cover_ends: False
preprocess_images: True
...
```

For more details, refer to the [Custom and Default Options](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/ocr.md) Section.



## How to Run

1. Edit and replace the `input.yaml` file in the [OCR folder](https://github.com/miielab/miienlp/tree/main/miienlp/ocr/input_yamls).
2. Run the pipeline:
    ```
    $ python src/main.py
    ```




