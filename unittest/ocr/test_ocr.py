import pytest
import sys, os
sys.path.insert(0, '../../miienlp/ocr/')
from ocr import OCR
from scan_GV import ScanGV
from main_text_classification import MainTextClassification
from page_divide import PageDivide
import combine
import utils



class TestOCR:
    def test_keywords(self):
        # tests alternative keyword option for classifying cover/end page
        text = "This page is a cover page. It contains an ISBN number"
        GV = ScanGV("", "", 0.5, [], "", "", False)
        assert GV.keywords_decision(text) == 1

    def test_default_combined_self(self):
        input_dir = "test_data/bloomer"
        input_dir = utils.validate_data_dir(input_dir)
        output = utils.validate_create_output_dir("", input_dir)
        utils.remove_temp(output)
        print(output)
        #assert "/ocr_output" in output
        assert "/ocr_combined" in output
        
     def test_default_uncombined_self(self):
        input_dir = "test_data/bloomer"
        input_dir = utils.validate_data_dir(input_dir)
        output = utils.validate_create_output_dir("", input_dir)
        utils.remove_temp(output)
        print(output)
        #assert "/ocr_output" in output
        assert "/ocr_uncombined" in output
