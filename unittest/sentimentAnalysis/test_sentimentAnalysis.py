import pytest, sys, os
# sys.path.insert(0, '../../miienlp/sentimentAnalysis/src/')
sys.path.insert(0, '../src/')
import utils 
from inference import Inference 
from clean_text import CleanText

class TestSentiment(object):
    def test_sentiment1(self):
        # tests sentiment analysis for negative sentence
        sent = "The man had a horrible day at work."
        device = utils.connect_GPU()
        model, tokenizer = utils.load_model(device)
        inf = Inference([sent], None, model, device, tokenizer, None)
        assert inf.sentence_predict(model, tokenizer, sent, device) < 0
    
    def test_sentiment2(self):
        # tests sentiment analysis for positive sentence
        sent = "The woman had a great day at work."
        device = utils.connect_GPU()
        model, tokenizer = utils.load_model(device)
        inf = Inference([sent], None, model, device, tokenizer, None)
        assert inf.sentence_predict(model, tokenizer, sent, device) > 0
    
    def test_sentiment3(self):
        # tests categorization
        sent = "The woman had a mediocre day at work."
        ct = CleanText(category_file='../category/categories.csv')
        cat_sent, cat_results = ct.categorize_sentence(sent)
        assert "The female had a mediocre day at work" in cat_sent
    
    def test_sentiment4(self):
        # tests categorization with capital letters at end of sentence
        sent = "The woman works at Uber."
        ct = CleanText(category_file='../category/categories.csv')
        cat_sent, cat_results = ct.categorize_sentence(sent)
        assert "The female works at company" in cat_sent