# Optical Character Recognition (OCR)

**The data directory containing images of text is the only required input (cf. [test_scans](https://github.com/miielab/miienlp/tree/main/examples/test_data/test_scans)).  See [Custom and Default Options](https://github.com/patriChiril/miie_beta/blob/main/documentation/developer_documentation/ocr.md) section for more details.**

## Example of a default input.yaml file

```
---
raw_data_directory: test_data/test_scans 
...
```

## Example input.yaml file with all features
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






