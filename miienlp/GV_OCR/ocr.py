import sys, os, time
import utils
from preprocessing import Preprocess
from scan_GV import ScanGV
#from scan_tesseract import ScanTesseract
import combine
from main_text_classification import MainTextClassification
from text_model import TextClassification
from alive_progress import alive_bar
from tqdm import tqdm
import pandas as pd

class OCR(object):
    def __init__(self, data_dir, output_combined, output_uncombined, ocr_method, confidence, image_order, language, project_id, model_id, remove_cover_ends, preprocess):
        self.data_dir = data_dir
        self.output_dir = output_combined
        self.output_uncombined = output_uncombined
        self.ocr_method = ocr_method
        self.confidence = confidence
        self.image_order = image_order
        self.language = language
        self.project_id = project_id
        self.model_id = model_id
        self.successful = 0 # number of successful scans
        self.attempted = 0 # number of attempted scans
        self.existing = 0 # number of already existing scans
        self.remove_cover_ends = remove_cover_ends
        self.run_prep = preprocess

    def update_statistics(self, result):
        '''
        Keeps track of number of scans that are attempted, successful, and already existing
        '''
        if result == 0:
            self.existing += 1
        elif result: # result is True
            self.successful += 1
            self.attempted += 1
        else: # result is False
            self.attempted += 1

    def prep_files(self, abspath):
        '''
        Preprocesses image and sets up text filenaming for single page scan images
        '''
        # uncombined text files
        text_file = self.output_uncombined.join(abspath.rsplit(self.data_dir))
        text_file = os.path.splitext(text_file)[0]+".txt"
        if self.run_prep:
            prep_file = self.output_dir + "/preprocess".join(abspath.rsplit(self.data_dir))
            prep_file = os.path.splitext(prep_file)[0]+".jpg"
            prep = Preprocess(abspath, prep_file)
            prep.run_preprocessing()
            return prep_file, text_file
        else:
            return abspath, text_file

    def run_ocr_pipeline(self):
        '''
        Run entire OCR pipeline. Loop through input and create output structure, preprocess and scan each image, and combine 
        images into text files based on user specifications 
        '''
        start = time.time()
        for root, subdirs, files in os.walk(self.data_dir):
            if os.path.exists(self.output_dir.join(root.rsplit(self.data_dir)) + ".txt"):
                result = 0
                self.update_statistics(result)
                continue
            # create temporary preprocessing (preprocessed images) and text directories (uncombined text files)
            prep_structure = self.output_dir + "/preprocess" + root[len(self.data_dir):]
            utils.construct_output_dir(prep_structure)
            text_structure = self.output_uncombined + root[len(self.data_dir):]
            utils.construct_output_dir(text_structure)
            files = utils.sort_files(files, self.image_order, "image")
            for scan in files:
                # root = path to book
                abspath = os.path.join(root, scan)
                if not utils.validate_scan(abspath): # if scan is not a readable image
                    continue
                prep_file, text_file = self.prep_files(abspath)
                if self.ocr_method == "Google Vision":
                    text = ScanGV(prep_file, text_file, self.confidence, self.language, self.project_id, self.model_id)
                    result = text.run_GV()
                    if self.run_prep: os.remove(prep_file)
                    self.update_statistics(result)
                else:
                    # this still has to be implemented
                    text = ScanTesseract(prep_file, text_file)
                    text.run_tess()
            
            if files:
                out = self.output_dir.join(root.rsplit(self.data_dir))
                inp =  self.output_uncombined.join(root.rsplit(self.data_dir))
                # combine text from each directory into single text file
                if self.remove_cover_ends: # if removing cover/end pages, classify each page in book as cover/end or content page
                    main_text = TextClassification(inp, self.image_order)
                    files_to_combine_text = main_text.run_classification()
                    print("Content lies from pages " + str(files_to_combine_text[0]) + " to " + str(files_to_combine_text[-1]))
                else:
                    files_to_combine_text = files
                #combine.combine_text(inp, out, self.image_order, files_to_combine_text) 
                combine.combine_text(inp, out, self.image_order)

        # remove temporary files
        utils.remove_temp(self.output_dir+"/preprocess") # remove preprocessed folder
        if len(os.listdir(self.output_dir)) == 0:
            utils.remove_temp(self.output_dir) # output is a text file, not a directory 
        print("Number of already existing OCRs: " + str(self.existing))
        print("Number of attempted OCRs: " + str(self.attempted))
        print("Number of successful OCRs: " + str(self.successful))
        end = time.time()
        print("Run Time (sec):  " + str(end-start))


