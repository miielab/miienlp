import nltk, spacy
from nltk.corpus import wordnet
import utils
import pandas as pd

class SpecificWordCounts(object):
    def __init__(self, data, supp_data_path, subcats, method, spacy_dataset="en_core_web_sm", _type="LU"):
        self.data = data
        self.spacy_dataset = spacy_dataset
        self.method = method
        self.categories = utils.read_vocab_files(supp_data_path, subcats, _type)
        # TO DO: add method that does specific word counts without using packages

    def generate_spacy_data(self):
        '''
        Labels entities using SpaCy and returns dataset
        '''
        nlp = spacy.load(self.spacy_dataset)
        nlp.max_length = 4000000
        spacy_txt = nlp(self.data)
        return spacy_txt

    def count_freq_nltk(self):
        '''
        Counts the frequency of words that fall into each category using NLTK
        '''
        tokens = nltk.word_tokenize(self.data)
        total_counts = {}
        for tok in tokens:
            for key, words in self.categories.items():
                if tok in words:
                    if key in total_counts.keys():
                        total_counts[key] += 1
                    else:
                        total_counts[key] = 1
        # checks for missing keys, sets values to zero
        for key in self.categories.keys():
            if key not in total_counts.keys():
                total_counts[key] = 0
        return total_counts

    def count_freq_spacy(self, spacy_txt):
        '''
        Counts the frequency of words that fall into each category using Spacy
        '''
        total_counts = {}
        for tok in spacy_txt:
            for key, words in self.categories.items():
                if tok.text in words:
                    if key in total_counts.keys():
                        total_counts[key] += 1
                    else:
                        total_counts[key] = 1
        # checks for missing keys, sets values to zero
        for key in self.categories.keys():
            if key not in total_counts.keys():
                total_counts[key] = 0
        return total_counts

    def count_prop_nltk(self):
        '''
        Counts the number of individual specific words tokens (i.e. "hair":2000) and overall domain counts (i.e. "appearance":3100)
        '''
        data = self.data.lower()
        tokens = nltk.word_tokenize(data)
        total_counts = {}
        individual_counts = {}

        for key, words in self.categories.items():
            individual_counts[key] = {}
            for word in words:
                individual_counts[key].update({word:0})

        for key, words in self.categories.items():
            total_count = 0
            for word in words:
                count = tokens.count(word) 
                total_count += count
                individual_counts[key][word] = count
            total_counts[key] = total_count
        return total_counts, individual_counts
    
    def construct_df(self, d):
        '''
        Creates dataframe of category and counts
        '''
        df = pd.DataFrame(data=d, index=[0])
        return df.reindex(sorted(df.columns), axis=1)

    def construct_prop_df(self, data, key):
        '''
        Creates dataframe of proportions and sorts by the most commonly used words
        '''
        df = pd.DataFrame(data, columns=[key, 'count', 'percentage'])
        return df.sort_values(by=['percentage'], ascending=False)

    def normalize_counts(self, sub_dict):
        '''
        Normalizes a dictionary of counts for all specific words in a given category 
        (i.e. "female" category has counts normalized for "she", "her", "mother", etc)
        '''
        data = []
        total = sum(sub_dict.values(), 0)
        for word, count in sub_dict.items():
            perc = 0 if total == 0 else (count / total) * 100
            data.append([word, count, round(perc, 2)])
        data.append(['TOTAL', total, 0.]) if total == 0 else data.append(['TOTAL', total, 100.00])
        return data

    def run_pipeline(self, output_folder="", proportion=False):
        '''
        Runs specific word pipleine
        Proportion: a parameter that optionally outputs whether to include CSV files on which words "drive" (make up) a given category
        https://docs.google.com/spreadsheets/d/1pvU8KwOrxH22BSoGQywYcYoZXN5-R4SW2sq0G3ZYgDE/edit?usp=sharing
        '''
        if self.method == 'spacy':
            spacy_txt = self.generate_spacy_data()
            counts = self.count_freq_spacy(spacy_txt)
        else:
            counts = self.count_freq_nltk()
        if proportion:
            counts, individual_counts = self.count_prop_nltk()
            for key, sub_dict in individual_counts.items():
                data = self.normalize_counts(sub_dict)
                df = self.construct_prop_df(data, key)
                utils.save_results(df, output_folder + "_proportion_" + key + ".csv")
        return self.construct_df(counts)