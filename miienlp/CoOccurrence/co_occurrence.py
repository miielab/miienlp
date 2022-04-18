import pandas as pd
import numpy as np
import os
import utils

class Co_Occurrence(object):
    def __init__(self, text, groups, domains, output, method, window, subcats, scaled, difference):
        #self.temporal = temporal
        self.groups = utils.read_vocab_files(groups, subcats)
        self.domains = utils.read_vocab_files(domains, subcats)
        self.output = output
        self.method = method
        self.window = window
        self.df = 0
        self.counts = {}
        self.scaled = scaled
        self.df = pd.DataFrame()
        self.group_counts = None
        self.domain_counts = None
        self.sentences = utils.read_sentences(text)
        self.text = utils.read_text(text)
        self.difference = difference


    def run_cooccurrence(self):
        '''
        Create csv of co-occurrence counts for groups and domains
        '''
        cols = list(self.groups)
        rows = list(self.domains)
        self.df = pd.DataFrame(columns = cols, index = rows)
        self.df[:] = 0
        if self.scaled == "group":
            self.group_counts = dict.fromkeys(cols, 0)
        if self.scaled == "domain":
            self.domain_counts = dict.fromkeys(rows, 0)
        if self.method == "sentence":
            self.coocurrence_sentence()
        if self.method == "context":
            self.coocurrence_context()
        print(self.df)
        if self.scaled == "group":
            for group in cols:
                self.df[group] = self.df[group]/self.group_counts[group]
        if self.scaled == "domain":
            for domain in rows:
                 self.df.loc[domain] = self.df.loc[domain]/self.domain_counts[domain]
        if self.difference:
            self.compute_difference()
        print(self.df)
        self.save_co_occurrence()
        return

    def save_co_occurrence(self):
        '''
        Saves co-occurrence to a CSV file
        '''
        self.df.to_csv(self.output)

    def coocurrence_sentence(self):
        '''
        Create df of co-occurrence counts per sentence for group and domain
        '''
        for sentence in self.sentences:
            sent = set(sentence.split())
            self.cooccurrence_general(sent)
        return

    def coocurrence_context(self):
        '''
        Create df of co-occurrence counts per context for group and domain, using windows of self.window words
        '''
        text = self.text.split()
        for i in range(len(text)-self.window-1):
            context = text[i:(i+self.window)]
            context = set(context)
            self.cooccurrence_general(context)
        return

    def compute_difference(self):
        '''
        Computes the difference between two columns
        '''
        self.df['Difference'] = self.df[self.df.columns[0]] - self.df[self.df.columns[1]]

    def cooccurrence_general(self, context):
        '''
        Loop through groups and domains and see if there is co-occurrence with given set of words
        '''
        for group in list(self.groups):
            if group == "female_words":
                print(context)
                print(bool(context & self.groups[group]))

            if bool(context & self.groups[group]):
                if self.group_counts: self.group_counts[group] += 1
                for domain in list(self.domains):
                    if bool(context & self.domains[domain]):
                        self.df[group][domain] += 1
        if self.domain_counts:
            for domain in list(self.domains):
                if bool(context & self.domains[domain]):
                    self.domain_counts[domain] += 1
        return


