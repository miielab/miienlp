# Optical Character Recognition (OCR)
### Custom and default options:


| Input | Description |
| --- | --- |
| Raw Data Directory ***(required)*** | User filepath to raw scan data directory|
| Output Combined | User filepath for OCR output for combined files ***(default is /path/to/raw_data_dir/../ocr_output)*** |
| Output Uncombined | User filepath for OCR output for uncombined files (each OCR'd file is stored as a separate file) ***(default is /path/to/raw_data_dir/../ocr_output)*** |
| OCR Method | Tesseract or Google Vision ***(default is Tesseract)*** |
| Confidence Threshold | Value from 0-1 indicating confidence threshold per scan ***(default is 0.5)*** |
| Image Ordering | Ordering for images in a directory: alphabetical *(a.jpg, b.jpg, c.jpg)*,numerical *(1.jpg, 2.jpg, 3.jpg)*, dash_numerical *(book-1.jpg, book-2.jpg, book-3.jpg)*, or underscore_numerical *(book_1.jpg, book_2.jpg, book_3.jpg)* ***(default is underscore_numerical)*** |
| Language | List of languages present in the scans. If unknown, provide an empty list and allow auto-language-detection. Possible languages currently include English, Spanish, Chinese, and Hindi. Example input could be ["English", "Spanish"]. ***(default is empty list)***|
| Project ID | If using google vision, project ID for classifying main text vs cover/end text ***(default is None)***|
| Model ID | If using google vision, model ID for the trained model to classify main text vs cover/end text ***(default is None)*** |
| Remove Cover & Ends | Whether or not to use text model to identify and remove cover and end pages from text ***(default is False)*** |
| Preprocess Images | Whether or not to preprocess (compress, deskew) images before running OCR ***(default is False)*** | 


### Data Structure Details

The suggested image type is JPEG, but this platform supports [eleven image types](https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56).


If your input folder is "data", and structured as follows:

```
data
|
|-------> group1
|           |
|           |-------> book1
|                           |
|                           |-------> page_1.jpg
|                           |-------> page_2.jpg
|                           |-------> page_3.jpg
|                                              .
|                                              .
|                                              .
|-------> group2
            |
            |-------> book2
                            |
                            |-------> page_1.jpg
                            |-------> page_2.jpg
                            |-------> page_3.jpg
                                               .
                                               .
                                               .

```

Your output will be structured as shown below, where the order that images are combined and the location of the output are based on user inputs. The structure of the output will mirror that of the input, combining all images in the same directory into a single text file.
```
output
|
|-------> group1
|           |
|           |-------> book1.txt                                                                     
|                                              
|-------> group2
            |
            |-------> book2.txt

```
