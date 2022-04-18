import nltk, spacy, csv, string
from collections import Counter
import pandas as pd
import utils

class POSCounts(object):
    def __init__(self, data, pos, output_file, method="spacy"):
        self.data = data
        self.pos = pos
        self.output_file = output_file
        self.method = method # nltk or spacy

    def nltk_pos_counts(self, sent):
        '''
        Records relevant pos information using NLTK
        '''
        source_tok = nltk.word_tokenize(sent)
        source_pos = nltk.pos_tag(source_tok)
        pos = []
        for token in source_pos:
            pos.append([token[0], token[1]])
        return pos

    def spacy_pos_counts(self, text, spacy_dataset="en_core_web_lg"):
        '''
        Records relevant pos information using SpaCy
        '''
        #nlp = spacy.load(spacy_dataset)
        #self.spacy_text = nlp(text)
        pos = []
        for token in self.data:
            pos.append([token.text, token.pos_])
        return pos

    def construct_df(self, pos):
        '''
        Constructs entity dataframe, grouping by unique rows and in the case where a given entity has multiple tags, it stores the most popular tag
        '''
        df = pd.DataFrame(pos, columns=['entity', 'entity_tag'])
        grouped = df.groupby(["entity", "entity_tag"]).size().reset_index(name='freq') #groups by unique rows and adds frequency of each row
        grouped = grouped.sort_values('freq').drop_duplicates("entity", keep='last') # keeps the modal tags
        grouped.reset_index(drop=True, inplace=True)
        return grouped

    def filter_results(self, df):
        '''
        Filters results based on certain entity tags (i.e. if you only want specific parts of speechs)
        '''
        filtered_counts_df = df[df["entity_tag"].isin(self.pos)].reset_index(drop=True)
        return filtered_counts_df

    def run_pipeline(self):
        '''
        Stores POS counts
        '''
        if self.method == "spacy":
            pos = spacy_pos_counts(self.data)
        else:
            pos = self.nltk_pos_counts(self.data)
        grouped_df = self.construct_df(pos)
        if self.pos:
            filtered_df = self.filter_results(grouped_df)
            utils.save_results(filtered_df, self.output_file + '_filtered.csv')
            return filtered_df
        utils.save_results(grouped_df, self.output_file + '_full.csv')
        return grouped_df
