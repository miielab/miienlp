# Optical Character Recognition (OCR)

## What does it do?
This platform will perform OCR on images, converting images containing text into text files. Specifically, it will perform [Google Vision OCR](https://cloud.google.com/vision/docs/ocr). 

## OCR Software Comparison Review

Over the past ~5 years, researchers have consistently identified Google Cloud Vision OCR as the best technology for converting images to text. In one study, [Tafti et al.](https://www.researchgate.net/publication/310645810_OCR_as_a_Service_An_Experimental_Evaluation_of_Google_Docs_OCR_Tesseract_ABBYY_FineReader_and_Transym) compared the accuracy of Google Docs (now Google Vision), Tesseract, ABBYY FineReader, and Transym OCR methods for over one thousand images and 15 image categories, and found that Google Vision generally outperformed other methods. In particular, Google Vision’s accuracy with digital images was 4% better than any other method. Additionally, the standard deviation of accuracy for Google Vision was quite low, suggesting that the quality of OCR does not drastically change from one image to the next. [Han and Hickman](https://source.opennews.org/articles/so-many-ocr-options/) compared seven OCR tools and also found Google Vision to be superior, specifically when extracting results from low resolution images. In another study that focused on comparing results from multiple image formats (jpg, png, tiff, etc),  [Vijayarani and Sakila](https://www.researchgate.net/publication/281583162_Performance_Comparison_of_OCR_Tools) found that Google Docs surpassed all other OCR tools. While Google Vision is dominant, it is not free. A cost-free alternative technology, is Tesseract. While Tesseract's performance does not match that of Google Vision's, it is close.

**IMPORTANT** 

For more details, see:
- [example](https://github.com/miielab/miienlp/blob/main/examples/ocr_example.md) 
- [setup instructions for UChicago MiiE Lab RA ONLY](https://github.com/miielab/miienlp/blob/main/documentation/miie_ra_documentation/ocr.md)
- [setup instructions for running OCR locally](https://github.com/miielab/miienlp/blob/main/documentation/user_documentation/ocr.md)





