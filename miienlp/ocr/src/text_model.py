import pandas as pd
import io, os
from google.cloud import vision
from PIL import Image as im
import string
import re
import utils
from sklearn.ensemble import RandomForestClassifier

class TextClassification(object):
    def __init__(self, book, text_order):
        self.book = book
        self.pages = os.listdir(book)
        self.labels = []
        self.content_pages = []
        self.text_order = text_order
        self.RF = None

    def annotate_label_data(self, label):
        output = []
        for image in labels[labels["Label"] == label]["Full_Path"]:
            client = vision.ImageAnnotatorClient()
            if not os.path.exists(image):
                print(image + " path does not exist")
                continue
            with io.open(image, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            annotations = client.document_text_detection(image = image)
            if len(annotations.full_text_annotation.text) > 0:
                text = annotations.full_text_annotation.text
                output.append(text)
        return output

    def load_label_data(self):
        labels = pd.read_csv("page_labeling.csv")
        labels = labels[~labels["Book Path"].str.contains("split_corpora")]
        labels["Book Path"] = "/project2/adukia/miie/compressed_scans/"+labels["Book Path"].str.split("/").str[2] + "/" + labels["Book Path"].str.split("/").str[3].str[0:3] + "0/"+ labels["Book Path"].str.split("/").str[3]
        labels["Full Path"] = labels["Book Path"] + "/" + labels["Filename"]
        labels.columns = ["Path", "Filename", "Label", "Full_Path"]

        content_text = self.annotate_label_data(0)
        cover_text = self.annotate_label_data(1)
        x = pd.DataFrame()
        x["content"] = content_text
        x.to_csv("/home/adas7/OCR/src/content.csv", index = False)
        y = pd.DataFrame()
        y["cover"] = cover_text
        y.to_csv("/home/adas7/OCR/src/cover.csv", index = False)


    def create_model(self):
        content = pd.read_csv("/home/adas7/OCR/src/content.csv")
        cover = pd.read_csv("/home/adas7/OCR/src/cover.csv")
        features = pd.DataFrame(columns = ['label','n_words', 'n_sentences','p_punc', 'p_period',
                                          'p_numbers', 'n_numbers', 'n_newline',
                                          'p_capital', 'avg_wordline', 'n_isbn',
                                          'n_acknowledgements', 'n_author',
                                          'n_copyright', 'n_allrights', 'n_manufactured',
                                          'n_america', 'n_library', 'n_ed', 'n_$', 'n_USA',
                                          'n_chapter', 'n_http', 'n_printed', 'n_illustrated', 
                                          'n_digitized', 'n_archive', 'n_internet'])

        for page in cover['cover']:
            nword = len(page)
            nsentences = len(page.split("\n"))
            ppunc = 1 - (len(page.translate(str.maketrans('', '', string.punctuation))) / len(page))
            pperiod = 1 - (len(page.replace(".", "")) / len(page))
            pnumbers = 1 - (len(''.join([i for i in page if not i.isdigit()])) / len(page))
            nnumbers = len(''.join([i for i in page if i.isdigit()]))
            nnewline = page.lower().count("\n")
            pcapital = len(re.findall(r'[A-Z]',page)) / len(page)
            avgwordline = sum( map(len, page.split("\n")) ) / len(page.split("\n"))
            nisbn = page.lower().count("isbn")
            nacknowledgements = page.lower().count("acknowledgements")
            nauthor = page.lower().count("author")
            ncopyright = page.lower().count("copyright")
            nallrights = page.lower().count("all rights reserved")
            nmanufactured = page.lower().count("manufactured")
            namerica = page.lower().count("america")
            nlibrary = page.lower().count("library")
            ned = page.lower().count("ed")
            ndollar = page.lower().count("$")
            ndollar += page.lower().count("dollar")
            nUSA = page.lower().count("usa")
            nUSA += page.lower().count("u.s.a.")
            nUSA += page.lower().count("united states of america")
            nUSA += page.count("US")
            nUSA += page.count("U.S.")
            nchapter = page.lower().count("chapter")
            nhttp = page.lower().count("http")
            nprinted = page.lower().count("printed in")
            nillustrated = page.lower().count("illustrated")
            ndigitized = page.lower().count("digitized")
            narchive = page.lower().count("archive")
            ninternet = page.lower().count("internet")
            
            features = features.append({'label': 1,
                                        'n_words': nword,
                                        'n_sentences': nsentences,
                                        'p_punc': ppunc,
                                        'p_period': pperiod,
                                        'p_numbers': pnumbers,
                                        'n_numbers': nnumbers,
                                        'n_newline': nnewline,
                                        'p_capital': pcapital,
                                        'avg_wordline': avgwordline,
                                        'n_isbn': nisbn,
                                        'n_acknowledgements': nacknowledgements,
                                        'n_author': nauthor,
                                        'n_copyright': ncopyright,
                                        'n_allrights': nallrights,
                                        'n_manufactured': nmanufactured, 
                                        'n_america': namerica, 
                                        'n_library': nlibrary,
                                        'n_ed': ned,
                                        'n_$': ndollar,
                                        'n_USA': nUSA,
                                        'n_chapter': nchapter, 
                                        'n_http': nhttp,
                                        'n_printed': nprinted,
                                        'n_illustrated': nillustrated,
                                        'n_digitized':ndigitized, 
                                        'n_archive':narchive, 
                                        'n_internet': ninternet}, ignore_index = True)
        for page in content['content']:
            nword = len(page)
            nsentences = len(page.split("\n"))
            ppunc = 1 - (len(page.translate(str.maketrans('', '', string.punctuation))) / len(page))
            pperiod = 1 - (len(page.replace(".", "")) / len(page))
            pnumbers = 1 - (len(''.join([i for i in page if not i.isdigit()])) / len(page))
            nnumbers = len(''.join([i for i in page if i.isdigit()]))
            nnewline = page.lower().count("\n")
            pcapital = len(re.findall(r'[A-Z]',page)) / len(page)
            avgwordline = sum( map(len, page.split("\n")) ) / len(page.split("\n"))
            nisbn = page.lower().count("isbn")
            nacknowledgements = page.lower().count("acknowledgements")
            nauthor = page.lower().count("author")
            ncopyright = page.lower().count("copyright")
            nallrights = page.lower().count("all rights reserved")
            nmanufactured = page.lower().count("manufactured")
            namerica = page.lower().count("america")
            nlibrary = page.lower().count("library")
            ned = page.lower().count("ed")
            ndollar = page.lower().count("$")
            ndollar += page.lower().count("dollar")
            nUSA = page.lower().count("usa")
            nUSA += page.lower().count("u.s.a.")
            nUSA += page.lower().count("united states of america")
            nUSA += page.count("US")
            nUSA += page.count("U.S.")
            nchapter = page.lower().count("chapter")
            nhttp = page.lower().count("http")
            nprinted = page.lower().count("printed in")
            nillustrated = page.lower().count("illustrated")
            ndigitized = page.lower().count("digitized")
            narchive = page.lower().count("archive")
            ninternet = page.lower().count("internet")

            features = features.append({'label': 0,
                                        'n_words': nword,
                                        'n_sentences': nsentences,
                                        'p_punc': ppunc,
                                        'p_period': pperiod,
                                        'p_numbers': pnumbers,
                                        'n_numbers': nnumbers,
                                        'n_newline': nnewline,
                                        'p_capital': pcapital,
                                        'avg_wordline': avgwordline,
                                        'n_isbn': nisbn,
                                        'n_acknowledgements': nacknowledgements,
                                        'n_author': nauthor,
                                        'n_copyright': ncopyright,
                                        'n_allrights': nallrights,
                                        'n_manufactured': nmanufactured, 
                                        'n_america': namerica, 
                                        'n_library': nlibrary,
                                        'n_ed': ned,
                                        'n_$': ndollar,
                                        'n_USA': nUSA,
                                        'n_chapter': nchapter, 
                                        'n_http': nhttp,
                                        'n_printed': nprinted,
                                        'n_illustrated': nillustrated,
                                        'n_digitized':ndigitized, 
                                        'n_archive':narchive, 
                                        'n_internet': ninternet}, ignore_index = True)

        y = features['label']
        X = features.drop(['label'], axis = 'columns')
        self.RF = RandomForestClassifier(n_estimators=100)
        self.RF.fit(X, y)
        return


    def page_classification(self, page):
        '''
        Classify a single page as a content page, cover/end page, or unclear
        '''
        page = open(page, 'r').read()
        if len(page) == 0:
            return 1
        features = pd.DataFrame(columns = ['n_words', 'n_sentences','p_punc', 'p_period',
                                          'p_numbers', 'n_numbers', 'n_newline',
                                          'p_capital', 'avg_wordline', 'n_isbn',
                                          'n_acknowledgements', 'n_author',
                                          'n_copyright', 'n_allrights', 'n_manufactured',
                                          'n_america', 'n_library', 'n_ed', 'n_$', 'n_USA',
                                          'n_chapter', 'n_http', 'n_printed', 'n_illustrated',
                                          'n_digitized', 'n_archive', 'n_internet'])
        nword = len(page)
        nsentences = len(page.split("\n"))
        ppunc = 1 - (len(page.translate(str.maketrans('', '', string.punctuation))) / len(page))
        pperiod = 1 - (len(page.replace(".", "")) / len(page))
        pnumbers = 1 - (len(''.join([i for i in page if not i.isdigit()])) / len(page))
        nnumbers = len(''.join([i for i in page if i.isdigit()]))
        nnewline = page.lower().count("\n")
        pcapital = len(re.findall(r'[A-Z]',page)) / len(page)
        avgwordline = sum( map(len, page.split("\n")) ) / len(page.split("\n"))
        nisbn = page.lower().count("isbn")
        nacknowledgements = page.lower().count("acknowledgements")
        nauthor = page.lower().count("author")
        ncopyright = page.lower().count("copyright")
        nallrights = page.lower().count("all rights reserved")
        nmanufactured = page.lower().count("manufactured")
        namerica = page.lower().count("america")
        nlibrary = page.lower().count("library")
        ned = page.lower().count("ed")
        ndollar = page.lower().count("$")
        ndollar += page.lower().count("dollar")
        nUSA = page.lower().count("usa")
        nUSA += page.lower().count("u.s.a.")
        nUSA += page.lower().count("united states of america")
        nUSA += page.count("US")
        nUSA += page.count("U.S.")
        nchapter = page.lower().count("chapter")
        nhttp = page.lower().count("http")
        nprinted = page.lower().count("printed in")
        nillustrated = page.lower().count("illustrated")
        ndigitized = page.lower().count("digitized")
        narchive = page.lower().count("archive")
        ninternet = page.lower().count("internet")
        features = features.append({'n_words': nword,
                                    'n_sentences': nsentences,
                                    'p_punc': ppunc,
                                    'p_period': pperiod,
                                    'p_numbers': pnumbers,
                                    'n_numbers': nnumbers,
                                    'n_newline': nnewline,
                                    'p_capital': pcapital,
                                    'avg_wordline': avgwordline,
                                    'n_isbn': nisbn,
                                    'n_acknowledgements': nacknowledgements,
                                    'n_author': nauthor,
                                    'n_copyright': ncopyright,
                                    'n_allrights': nallrights,
                                    'n_manufactured': nmanufactured, 
                                    'n_america': namerica, 
                                    'n_library': nlibrary,
                                    'n_ed': ned,
                                    'n_$': ndollar,
                                    'n_USA': nUSA,
                                    'n_chapter': nchapter, 
                                    'n_http': nhttp,
                                    'n_printed': nprinted, 
                                    'n_illustrated': nillustrated, 
                                    'n_digitized':ndigitized, 
                                    'n_archive':narchive, 
                                    'n_internet': ninternet}, ignore_index = True)
        label = self.RF.predict(features)[0]
        if "digitized by the internet archive" in page.lower(): 
            label = 1
        elif "http" in page.lower():
            label = 1
        elif "about the author" in page.lower():
            label = 1
        elif "acknowledge" in page.lower():
            label = 1
        elif "all rights reserved" in page.lower():
            label = 1
        elif "CONTENT" in page.lower():
            label = 1
        elif "chapter" in page.lower():
            label = 0
        elif "author's note" in page.lower():
            label = 1
        elif "glossary" in page.lower():
            label = 1
        elif "illustrated by" in page.lower():
            label = 1
        elif "biographical notes" in page.lower():
            label = 1
        elif "copyright" in page.lower():
            label = 1
        elif "printed in" in page.lower():
            label = 1
        elif "isbn" in page.lower():
            label = 1

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
            for i in range(1, len(self.labels) // 3):
                ratio = sum(self.labels[0:i]) / len(self.labels[0:i])
                front_ratios.append(ratio)
            for i in range(len(self.labels)-1, len(self.labels)//3, -1):
                ratio = sum(self.labels[i:]) / len(self.labels[i:])
                back_ratios.append(ratio)
            for i in range(0, len(self.labels) // 3):
                if self.labels[i] == 0 and self.labels[i+1] == 0:
                    if self.labels[i+2] == 0:
                        content_start = i
                        break
                    if self.labels[i+2] == 1 and self.labels[i+3] == 0:
                        content_start = i
                        break
            for i in range(len(self.labels)-1, len(self.labels)//3 -1):
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
                    last_0 = len(self.labels) - self.labels[::-1].index(0) - 1
                except:
                    last_0 = len(self.labels)
                content_end = last_0
            content_end = content_end + 1
            self.content_pages = self.pages[content_start:content_end]
            if len(self.content_pages) == 0:
                self.content_pages = self.pages
            return

    def run_classification(self):
        '''
        Create list of labels for each page in text
        '''
        #self.load_label_data()
        self.create_model()
        self.pages = utils.sort_files(self.pages, self.text_order, "text")
        for page in self.pages:
            page_path = os.path.join(self.book, page)
            if not page.split(".")[1] == "txt": # if file is not a text file
                print(page_path + "is not a text file")
                continue
            self.labels.append(self.page_classification(page_path))
        self.get_content_pages()
        return self.content_pages 






