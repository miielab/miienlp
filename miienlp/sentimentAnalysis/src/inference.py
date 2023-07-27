# importing modules
import numpy as np
import pandas as pd

class Inference(object):
    def __init__(self, sentences, output_file, model, device, tokenizer, ct):
        # storing user input values for sentences and output file path
        self.sentences = sentences
        self.output_file = output_file
        self.model = model
        self.device = device
        self.tokenizer = tokenizer
        self.clean_text = ct

    ### Combines sentiment, sentences, and category tags to create output csv
    def create_output(self):

        # create a list to keep track of results
        sentiment_results = []

        # create lists of sentences, altered sentences, sentiment, categories
        # sentences is self.sentences
        sentiments, categories, altered_sentences = self.make_sentence_predictions(self.sentences)
       
        # adding sentences, altered sentences, sentiment, and categories to a list to be later
        # converted into a dataframe
        for i in range(len(self.sentences)):
            sentiment_results.append([self.sentences[i], altered_sentences[i], sentiments[i], categories[i]])

        # create a df to save and return
        df = pd.DataFrame(sentiment_results, columns=["sentence", "altered_sentences", "sentiment", "category_tags"])
        df.to_csv(self.output_file)
        return df

    ### Predict the sentiment of a single sentence using the trained BERT model
    def sentence_predict(self, model, tokenizer, sentence, device):
               
        # put the model into evaluation mode to disable dropout layers
        model.eval()

        # send model to device
        model.to(device)
        
        # tokenize the sentence
        inputs = tokenizer(sentence, return_tensors='pt')
        input_ids = inputs.input_ids.to(device)
        attn_mask = inputs.attention_mask.to(device)
        
        # make predictions
        outputs = model(input_ids, attn_mask)
        
        # get probabilities as a numpy array
        probs = outputs[0].cpu().detach().numpy()
        
        # calculate sentiment score
        # this depends on the index of probs that contains the largest probability
        sentiment_score = (np.argmax(probs) - 2) / 2

        # return sentiment score
        return sentiment_score
    
    ### Use `sentence_predict` to calculate sentiment of all sentences from input. Returns a list of sentiment values.
    def make_sentence_predictions(self, sentences):

        # creating an empty list of sentiment values, an empty list of category tags, and an empty list of sentences
        sentiment_values = []
        category_tags = []
        altered_sentences = []

        # iterating through all sentences; calculating sentiment of each
        for sent in sentences:

            # clean the sentence and find the category tags
            sent, categories = self.clean_text.categorize_sentence(sent)

            # adding list of categories mentioned in this sentence to overall list of category tags
            category_tags.append(categories)

            # adding altered sentences to altered sentence list
            altered_sentences.append(sent)
            
            # find the sentiment of the sentence
            sentiment_values.append(self.sentence_predict(model=self.model, 
                                                          tokenizer=self.tokenizer, 
                                                          sentence=sent, 
                                                          device=self.device))
        
        # returning list of sentiment values, category tags, and altered sentences
        return sentiment_values, category_tags, altered_sentences