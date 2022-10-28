import os
from google.cloud import automl
import cv2
import io
import utils


class MainTextClassification(object):
    def __init__(self, book, pages, project_id, model_id):
        self.book = book
        self.pages = pages
        self.project_id = project_id
        self.model_id = model_id
        self.labels = []
        self.content_pages = []


    def page_classification(self, content):
        '''
        Classify a single page as a content page, cover/end page, or unclear
        '''
        with io.open(content, 'rb') as image_file:
            im = image_file.read()
        prediction_client = automl.PredictionServiceClient()
        model_full_id = automl.AutoMlClient.model_path(self.project_id, "us-central1", self.model_id)
        image = automl.Image(image_bytes=im)
        payload = automl.ExamplePayload(image=image)
        params = {"score_threshold": "0.5"}
        request = automl.PredictRequest(name=model_full_id, payload=payload, params=params)
        response = prediction_client.predict(request=request)
        for result in response.payload:
            label = int(result.display_name) # cover/end = 1, content = 0
            classification_score = result.classification.score
        #if classification_score > 0.85:
        #    return label
        #else:
        #    return "unclear"
        return label

    def get_content_pages(self):
        '''
        Extract all content pages given the labels
        '''
        if len(self.labels) < 4: # if there are less than 4 pages, we can assume no cover/end pages
            return self.pages
        else:
            front_ratios = []
            back_ratios = []
            content_start = "starting"
            content_end = "ending"
            for i in range(1, len(self.labels) // 2):
                ratio = sum(self.labels[0:i]) / len(self.labels[0:i])
                front_ratios.append(ratio)
            for i in range(len(self.labels)-1, len(self.labels)//2, -1):
                ratio = sum(self.labels[i:]) / len(self.labels[i:])
                back_ratios.append(ratio)
            for i in range(0, len(self.labels) // 2):
                if self.labels[i] == 0 and self.labels[i+1] == 0:
                    if self.labels[i+2] == 0:
                        content_start = i
                        break
                    if self.labels[i+2] == 1 and self.labels[i+3] == 0:
                        content_start = i
                        break
            for i in range(len(self.labels)-1, len(self.labels)//2, -1):
                if self.labels[i] == 0 and self.labels[i-1] == 0:
                    if self.labels[i-2] == 0:
                        content_end = i
                        break
                    if self.labels[i-2] == 1 and self.labels[i-3] == 0:
                        content_end = i
                        break
            
            if content_start == "starting":
                try:
                    first_0 = self.labels.index(0)
                except:
                    first_0 = len(self.labels)
                content_start = first_0
            if content_end == "ending":
                try:
                    last_0 = len(labels) - labels[::-1].index(0) - 1
                except:
                    last_0 = len(labels)
                content_end = last_0
            content_end = content_end + 1
            self.content_pages = self.pages[content_start:content_end]
            return
            
            

    def run_classification(self):
        '''
        Create list of labels for each page in text
        '''
        for page in self.pages:
            page_path = os.path.join(self.book, page)
            if not utils.validate_scan(page_path): # if scan is not a readable image
                print(page_path + "is not a a valid scan.")
                continue
            self.labels.append(self.page_classification(page_path))
        self.get_content_pages()
        return self.content_pages

        
