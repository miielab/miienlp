import os
import re
import string
import sys

import pandas as pd
import spacy

import utils


class NER(object):
    def __init__(self, data, filter_entities, spacy_dataset="en_core_web_sm"):
        self.data = data
        self.filter_entities = filter_entities
        self.spacy_dataset = spacy_dataset

    def generate_spacy_data(self):
        """
        Labels entities using SpaCy and returns dataset
        """
        nlp = spacy.load(self.spacy_dataset)
        nlp.max_length = 4000000
        spacy_txt = nlp(self.data)
        return spacy_txt

    def extract_entities(self, spacy_txt):
        """
        Generates a list of all the entities detected in a text and their corresponding labels
        """
        entities = []
        for ent in spacy_txt.ents:
            entities.append([ent.text, ent.label_])
        return entities

    def clean_entities(self, entities):
        """
        Cleans entities
        """
        punc = (
            string.punctuation.replace("-", "").replace(".", "").replace("'", "") + "¿"
        )  # want to include dashes and periods as they are frequently apart of names
        # lead_trail_punc = string.punctuation + "¿"
        # add apostrophes to the above line (they might show up in names)
        clean_entities = []
        for ent, tag in entities:
            text = ent.lower().strip()  # lowers text and removes extraneous white space
            if (
                text[-2:] == "'s" or text[-2:] == "’s"
            ):  # removes possessive parts of words
                text = text[:-2]
            text = text.translate(
                str.maketrans("", "", punc)
            )  # removing certain punctuation
            text = text.replace("\n", "")  # removing newline characters
            text = re.sub(r"\d+", "", text)  # removes digits
            text = text.lstrip(string.punctuation + "¿")
            text = text.rstrip(string.punctuation.replace(".", "") + "¿")
            # text = text.strip(string.punctuation + "¿")  # TO DO: remove any leading punctuation
            text = re.sub(" +", " ", text)  # TO DO: remove double spaces
            text = text.strip()  # removes any final extraneous white space
            if len(text) > 1:
                clean_entities.append([text, tag])
        return clean_entities

    def construct_df(self, entities):
        """
        Constructs entity frequency dataframe, grouping by unique rows and in the case where a given entity has multiple tags, it stores the most popular tag

        TO DO: this function needs to be fixed for Emileigh's NER analysis
        """
        df = pd.DataFrame(entities, columns=["entity", "modal_tag"])
        grouped = (
            df.groupby(["entity", "modal_tag"]).size().reset_index(name="freq")
        )  # groups by unique rows and adds frequency of each row
        grouped = grouped.sort_values("freq").drop_duplicates(
            subset=["entity", "modal_tag"], keep="last"
        )  # keeps the modal tags, TO DO: keep the frequency of the duplicates that will be dropped so that we have total frequency
        grouped.reset_index(drop=True, inplace=True)
        return grouped

    def filter_results(self, df):
        """
        Filters results based on certain entity tags (i.e. if you only want PERSON entities)
        """
        # filtered_counts_df = df[df["modal_tag"].isin(self.filter_entities)].reset_index(drop=True)
        filtered_counts_df = df[df["modal_tag"].isin(self.filter_entities)].reset_index(
            drop=True
        )
        return filtered_counts_df

    def run_pipeline(self):
        """
        Runs NER pipeline and saves results
        """
        # TO DO: fix this method, have it take in inputs instead of the constructor?
        spacy_txt = self.generate_spacy_data()
        entities = self.extract_entities(spacy_txt)
        clean_entities = self.clean_entities(entities)

        df = self.construct_df(clean_entities)
        if self.filter_entities:
            return self.filter_results(df)
        return df
