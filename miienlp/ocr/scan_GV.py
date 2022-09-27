from google.cloud import vision
import io, os
from PIL import Image as im
from main_text_classification import MainTextClassification


class ScanGV(object):
    def __init__(self, scan, output, confidence, language, project_id, model_id, remove_cover_ends):
        self.file = scan
        self.output = output
        self.threshold = 0.2
        self.language = language # should be a list of languages: ["English", "Spanish"]
        self.project_id = project_id
        self.model_id = model_id
        self.remove_cover_ends = remove_cover_ends

    def run_GV(self):
        '''
        OCR's an image and saves the output to a text file. If the confidence of the scan does not meet the user's
        threshold, then it does not include the scan. User can also specify the language the text is in to help GV
        read the text
        '''
        # do not run if file already exists
        if os.path.exists(self.output):
            return 0, None
        client = vision.ImageAnnotatorClient()
        with io.open(self.file, 'rb') as image_file:
            content = image_file.read()
        label = 0
        image = vision.Image(content=content)
        if self.language: # if language is specified, use it to help GV read text
            annotations = client.document_text_detection(image = image, image_context={"language_hints": self.language})
        else: # if language is not specified, allow GV to automatically try and detect the language
            annotations = client.document_text_detection(image = image)
        if label == "unclear":
            label = self.keywords_decision(annotations.full_text_annotation.text)
            if label == 1:
                print(self.file + " is not a content page. Not including.")
                return False, label
        confidence = self.confidence(annotations)
        if confidence < self.threshold:
            print("Scan did not meet confidence threshold of "+ self.threshold + " and therefore was unsuccessful: " + self.file)
            return False, label
        if len(annotations.full_text_annotation.text) > 0:
            text = annotations.full_text_annotation.text
            text_output = open(self.output, "w+")
            text_output.write(text)
            text_output.close()
        if annotations.error.message:
            raise Exception('{}\nFor more info on error messages, check: ''https://cloud.google.com/apis/design/errors'.format(response.error.message))
        print("Successfully OCR'd " + self.file + " with confidence = " + str(confidence))
        return True, label

    def confidence(self, annotations):
        '''
        Gets confidence of each block of text in an image, and return average confidence of blocks
        '''
        confidence = []
        for page in annotations.full_text_annotation.pages:
            for block in page.blocks:
                confidence.append(block.confidence)
        return sum(confidence) / len(confidence)

    def keywords_decision(self, text):
        '''
        If the score of the prediction is not above a specific threshold (0.85), then
        we look at keywords present in the text to make the classification
        '''
        label = 0
        text = text.lower()
        if "author's note" in text or "isbn" in text:
            label = 1
        return label
