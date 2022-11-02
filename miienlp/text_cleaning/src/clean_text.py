import sys, os, json, re
import pandas as pd
import spacy
import nltk
import Levenshtein as lev
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import utils
import string
import unicodedata
import unidecode
from alive_progress import alive_bar


class CleanText(object):
	def __init__(self, raw_text, ngram_file = None, lemmatize = False, stopwords_file = False, categorize_domain_file = None, categorize_domain_subcats = [], fuzzy = True, threshold_fuzzy = 0.9, categorize_famous_file = None, categorize_famous_subcats = [], standardize_file = None, gender_ssa_file = None, digits = False, stopwords_add = [], stopwords_remove = [], lower = False, special_characters = False, spacy_dataset_type = "en_core_web_lg", case_sensitive = False):
		self.raw_text = raw_text
		self.ngram_lst = utils.load_ngram_file(ngram_file) if ngram_file else []
		self.stopwords = utils.load_custom_stopwords(stopwords_file) if stopwords_file else set() #set(stopwords.words('english'))
		self.add_stopwords(stopwords_add)
		self.remove_stopwords(stopwords_remove)
		self.ssa_df = utils.load_ssa_file(gender_ssa_file) if gender_ssa_file else None
		self.standardize_df = utils.load_standardize_file(standardize_file) if standardize_file else None
		self.digits = digits
		self.lemmatize = lemmatize
		self.categorize_domain = utils.load_categorize_file(categorize_domain_file, categorize_domain_subcats) if categorize_domain_file else {}
		self.categorize_famous = utils.load_categorize_file(categorize_famous_file, categorize_famous_subcats) if categorize_famous_file else {}
		self.case_sensitive = case_sensitive
		self.lower = lower
		self.fuzzy = fuzzy
		self.threshold = threshold_fuzzy
		self.special_characters = special_characters
		self.spacy_dataset_type = spacy_dataset_type

	def remove_stopwords(self, words):
		'''
		Removes stopwords from the stopword list
		'''
		# TO DO: if you are removing stopwords from a custom txt file, remove from both the file and the attribute in the class
		self.stopwords.difference_update(set(words))

	def add_stopwords(self, words):
		'''
		Adds stopwords to the stopword list
		'''
		# TO DO: if you are adding stopwords to a custom txt file, add them both to the file and the attribute in the class
		self.stopwords.update(set(words))

	def classify_gender_name(self, name):
		'''
		Classifies gender based on name for spacy entities (name can have multiple tokens, i.e. "Joe Smith")
		'''
		m_titles = set(['Mr', 'Mister', 'Sir'])
		f_titles = set(['Mrs', 'Miss', 'Ms', 'Missus'])
		name_list = name.split()
		# keeps looping through all tokens in the name_list until a token appears in the ssa dataset, or returns None
		for name in name_list:
			if name in m_titles: return "male"
			elif name in f_titles: return "female"
			try:
				gender_series = (self.ssa_df.loc[self.ssa_df["name"] == name])["gender"]
				return gender_series.iloc[0].lower()
			except:
				continue
		return None

	def categorize_word(self, word, category):
		'''
		Categorizes a word based on the categorize file for famous or domain categorization
		'''
		for key, _set in category.items():
			if self.fuzzy and category == self.categorize_famous:
				for potential_match in _set:
					if lev.ratio(word.lower(), potential_match) >= self.threshold:
						return key.lower()
			else:
				if self.case_sensitive:
					if word.lower() in _set or word in _set:
						return key.lower()
				else:
					_set_lower = list(map(lambda x: x.lower(), _set))
					if word.lower() in _set_lower:
						return key.lower()

		return None

	def combine_ngrams(self, sent):
		'''
		Combines interesting ngrams into one word based on the items in the self.ngram_lst
		'''
		for ngram in self.ngram_lst:
			if ngram in sent.lower():
				sent = re.sub(ngram, ngram.replace(" ", "_"), sent, flags=re.IGNORECASE)
		return sent

	def generate_spacy_params(self):
		'''
		Labels entities using SpaCy and returns dataset
		'''
		if self.spacy_dataset_type:
			nlp = spacy.load(self.spacy_dataset_type)
			nlp.max_length = 4000000
			return nlp
		else:
			return None

	def categorize_race_famous(self, spacy_text):
		'''
		Categorizes famous people into race_gender
		'''
		categorized_sent = str(spacy_text)
		for ent in spacy_text.ents:
			if ent.label_ == "PERSON":
				word = ent.text.strip()
				gender_race_result = self.categorize_word(word, self.categorize_famous)
				if gender_race_result is not None:
					try:
						categorized_sent = re.sub(str(ent), gender_race_result, categorized_sent, flags=re.IGNORECASE)
					except:
						print("Entity {} is not able to be categorized".format(str(ent)))
		return categorized_sent

	def categorize_gender(self, spacy_text):
		'''
		Categorizes people into their gender
		'''
		categorized_sent = str(spacy_text)
		for ent in spacy_text.ents:
			if ent.label_ == "PERSON":
				word = ent.text.strip()
				gender_result = self.classify_gender_name(word)
				if gender_result is not None:
					try:
						categorized_sent = re.sub(str(ent), gender_result, categorized_sent, flags=re.IGNORECASE)
					except:
						print("Entity {} is not able to be categorized".format(str(ent)))
		return categorized_sent

	def get_wordnet_pos(self, pos_tag):
		'''
		Map POS tag to first character lemmatize() accepts
		Converts Tree Bank POS tags to wordnet compatible tags
		'''
		tag_dict = {"J": wordnet.ADJ,
					"N": wordnet.NOUN,
					"V": wordnet.VERB,
					"R": wordnet.ADV}
		return tag_dict.get(pos_tag, wordnet.NOUN) # in case of missing key, assume word is noun


	def write_output(self, output_file, sentences):
		'''
		Writes output
		'''
		with open(output_file, 'w+') as f:
			f.write('\n'.join(sentences))
			#f.writelines(sentences)
		return 0

	def clean_sentence(self, sent, lemmatizer = False, nlp = None):
		sent = re.sub("-\n", "", sent) # removing line breaks
		sent = re.sub("\n", " ", sent) # removing any excess newline characters
		sent = unicodedata.normalize('NFKD', sent)
		sent = sent.encode("ASCII", "ignore").rstrip().strip().decode("utf-8") # removes non-ascii characters

		if self.special_characters: sent = sent.replace("'", " ")
		if self.standardize_df is not None:
			# TO DO: This is being called on every sentence, whether or not the word even appears in the sentence - inefficient
			for index, row in self.standardize_df.iterrows():
				sent = re.sub(row[0], row[1], sent)
		if self.ngram_lst: sent = self.combine_ngrams(sent)
		if nlp:
			spacy_text = nlp(sent)
			if self.categorize_famous:
				sent = self.categorize_race_famous(spacy_text)
			spacy_text = nlp(sent)
			if self.ssa_df is not None:
				sent = self.categorize_gender(spacy_text)
			sent = sent + '\n'
		if self.categorize_domain or self.lemmatize or self.stopwords:
			clean_words = []
			words = word_tokenize(sent) # TO DO: find spacy equivalent
			words_pos = nltk.pos_tag(words) # TO DO: find spacy equivalent
			for word, pos in words_pos:
				if lemmatizer:
					word = lemmatizer.lemmatize(word, self.get_wordnet_pos(pos[0]))
				if word.lower() not in self.stopwords and (word.lower() == 'a' or word.lower() == 'i' or len(word) > 1):
					if self.categorize_domain:
						cat_word = self.categorize_word(word, self.categorize_domain)
						if cat_word is not None: word = cat_word
					clean_words.append(word)
			sent = ' '.join(clean_words)
		if self.special_characters: sent = re.sub(r'([^_\s\w])+', ' ', sent) # removes special characters (punctuation)
		if self.digits:
			sent = re.sub(r'\d+', '', sent) # removes digits
			# sent = re.sub(r'(?i)(?=\b[MCDXLVI]{1,6}\b)M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})', 'digit', sent) # removes roman numerals
		if self.lower: sent = sent.lower()

		sent = re.sub(r'\s+', ' ', sent) # removing extraneous spaces in the sentence
		sent = sent.strip().rstrip() # removes excess whitespaces
		if re.match(r'^[_\W]+$', sent): sent = ''# removing sentences that contain only special characters
		return sent

	def clean_text_file(self, output_file):
		'''
		Cleans a text file given cleaning specifications
		'''
		sentences = sent_tokenize(self.raw_text) # split data into sentences (TO DO: Try to find a spacy function for this)
		lemmatizer = WordNetLemmatizer() if self.lemmatize else False
		nlp = self.generate_spacy_params()
		new_sentences = []
		with alive_bar(len(sentences), bar="blocks") as bar:
			for sent in sentences:
				new_sentence = self.clean_sentence(sent, lemmatizer, nlp)
				if len(new_sentence) != 0:
					new_sentences.append(new_sentence)
				bar()
		self.write_output(output_file, new_sentences)
		return
