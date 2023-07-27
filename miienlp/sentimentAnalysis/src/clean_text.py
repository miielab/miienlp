import re
import Levenshtein as lev
import utils

### Used to clean a sentence (replace words with category names)
class CleanText(object):
	def __init__(self, category_file = None, fuzzy = True, threshold_fuzzy = 0.9, case_sensitive = False):
		self.categories = utils.load_categorize_file(category_file)
		self.case_sensitive = case_sensitive
		self.fuzzy = fuzzy
		self.threshold = threshold_fuzzy

	### Categorize a word based on the input categories file
	def categorize_word(self, word, category):
		for key, _set in category.items():

			# fuzzy: if the word found matches a word in the category's items by a certain percentage (threshold), replace the word
			if self.fuzzy:
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

	### Categorizes words in a sentence into any type of category; returns updated sentence and a list of word categories
	def categorize_sentence(self, text):
		categorized_sent = str(text)
		categorized_results = []
		for word in text.split():
			word = word.strip()
			if word[-1] == '.':
				word = word[:-1]
			categorize_result = self.categorize_word(word, self.categories)
			if categorize_result is not None:
				try:
					categorized_sent = re.sub(str(word), categorize_result, categorized_sent, flags=re.IGNORECASE)
					categorized_results.append(categorize_result)
				except:
					print("The word {} is not able to be categorized".format(str(word)))
		return categorized_sent, categorized_results

### creating an exception to throw if there is no .csv file in the 'category_dir' path in the input.yaml file
class noCSVException(Exception):
	def __init__(self, message="There is no .csv file to get category information from."):
		self.message = message
		super().__init__(self.message)