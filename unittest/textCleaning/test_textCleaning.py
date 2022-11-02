import pytest
import sys
from nltk.corpus import stopwords
sys.path.insert(0, '../../miienlp/text_cleaning/src/')
from clean_text import CleanText
import utils
from nltk.stem import WordNetLemmatizer

d1 = {
	"data_directory": "test_data",
 	"stopwords_file": "sample_inputs/stopwords_test_files/stopwords.txt",
 	"ngrams_file": "sample_inputs/ngram_test_files/ngrams.txt",
 	"categorize_file": "sample_inputs/categorize_test_files/categorize.csv",
 	"digits": False,
	"output_preference":"Vectors",
  	"output_filenames": ["", ""],
  	"standardized_file" :"sample_inputs/standardize_test_files/standardize.csv"
}

d2 = {
	"categorize": "/project2/adukia/miie/text_analysis/supplemental_data/Categories/",
	"subcats": ["family", "unpleasant", "positive", "pleasant", "negative", "negative_emotions"]
}

class TestTextCleanClass:
	def test_digits1(self):
		# tests that digits are not removed unless specified
		clean = CleanText("", lower=True, special_characters = True)
		sent = "The first section is Section iv. and 12 and it is dumb."
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "the first section is section iv and 12 and it is dumb"

	def test_digits2(self):
		# tests that digits are removed when requested for clean counts
		clean = CleanText("", digits=True)
		sent = "THE COW\nwent over the moon!!!!...1234 Section I."
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "THE COW went over the moon!!!!... Section I."

	def test_spec_characters(self):
		# tests that non-ascii special characters are always removed
		clean = CleanText("", digits=False)
		sent = "hello <% 长 花式 杂、 * 光 乐 长 次 * * 次 6 ☆☆wow ánjálí ñaña???"
		cleaned = clean.clean_sentence(sent)
		assert cleaned == 'hello <% * * * 6 wow anjali nana???'
	'''
	def test_categorize1(self):
		# tests whether categorize CSV is properly read into a dictionary
		clean = CleanText("", categorize_domain_file=d1["categorize_file"])
		assert isinstance(clean.categorize_domain, dict)

	def test_categorize2(self):
		# tests whether the constructed categorize dictionary contains the correct keys
		clean = CleanText("", categorize_famous_file=d1["categorize_file"])
		assert set(list(clean.categorize_famous.keys())) == set(["male", "female", "fruit"])


	def test_categorize3(self):
		# tests categorization in the clean sentence function
		clean = CleanText("", categorize_domain_file=d1["categorize_file"], lower=True)
		clean.add_stopwords(["the", "who"])
		sent = "the Boy loved the GIRL who ate mango 1234"
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "male loved female ate fruit 1234"
	'''
	def test_contractions(self):
		# tests that words with contractions have punctuation appropriately handled
		clean = CleanText("", special_characters = True, stopwords_add=["s", "t", "d", "m", "ll", "re", "ve"])
		sent = "I couldn't believe what I've become"
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "I couldn believe what I become"
	
	def test_contractions2(self):
		# tests that words with contractions have punctuation appropriately handled
		clean = CleanText("", special_characters = True, stopwords_add=["s", "t", "d", "m", "ll", "re", "ve"])
		sent = "This was Sophia's favorite part"
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "This was Sophia favorite part"

	def test_stopwords1(self):
    	# tests variable type of stopwords
		clean = CleanText("", stopwords_file=d1["stopwords_file"])
		assert type(clean.stopwords) == set

	def test_stopwords2(self):
		# tests that stopwords reverts to default nltk stopwords if invalid file provided
		clean = CleanText("", stopwords_file="blah.txt")
		assert clean.stopwords == set(stopwords.words('english'))

	def test_ngrams1(self):
		# tests variable type of ngram_lst
		clean = CleanText("", ngram_file=d1["ngrams_file"])
		assert type(clean.ngram_lst) == list

	def test_ngrams2(self):
		# tests ngram list is empty if invalid file provided
		clean = CleanText("", ngram_file="ngramfile")
		assert clean.ngram_lst == []

	def test_ngrams3(self):
		# tests whether ngrams list contains the correct contents
		clean = CleanText("", ngram_file=d1["ngrams_file"], lower=True, special_characters=True)
		sent = "George Washington was friends with Abraham Lincoln's dog and Martin Luther King Junior Also"
		sent = clean.clean_sentence(sent)
		assert sent == "george_washington was friends with abraham_lincoln s dog and martin_luther_king_junior also"

	def test_line_break1(self):
		clean = CleanText("", digits=True, lower=True)
		sent = "It should not be fur-\nnished like that"
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "it should not be furnished like that"

	def test_clean_sentence1(self):
		# tests function of clean_sentence function for lexicon counts, using default settings
		clean = CleanText("")
		sent = "THE COW\nwent over the moon!!!!...1234"
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "THE COW went over the moon!!!!...1234"

	def test_clean_sentence2(self):
		# tests function of clean_sentence function for vec counts, using default settings
		clean = CleanText("", digits=True, lower=True, special_characters = True)
		sent = "THE COW\nwent over a moon and I like moons b!!!!...1234!@#$%^&*()|}{':<>,./?~`+=- 后"
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "the cow went over a moon and i like moons b"

	def test_clean_sentences3(self):
		# tests the removal of extraneous whitespaces
		clean = CleanText("")
		sent = "     hello!   how are you   "
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "hello! how are you"

	def test_clean_sentences3(self):
		# tests the removal of lines only containing spaces and special characters
		clean = CleanText("")
		sent =  " .."
		cleaned = clean.clean_sentence(sent)
		assert cleaned == ""
	
	def test_standardization1(self):
		# for bundled constructs
		clean = CleanText("", standardize_file=d1["standardized_file"])
		sent = "Martin Luther King Jr. Martin Luther King Jr Martin Luther King's Honest Abe. and Al Capone's, said that Douglas Fairbanks's! house was nice and Dr. Martin Luther King Jr."
		cleaned = clean.clean_sentence(sent)
		print(cleaned)
		assert cleaned == "martin_luther_king_junior martin_luther_king_junior Martin Luther King's abraham_lincoln and al_capone, said that douglas_fairbanks! house was nice and martin_luther_king_junior"

	def test_lemmatize1(self):
		# tests whether lemmatization works in clean sentence
		clean = CleanText("", lower=True, lemmatize = True)
		lemmatizer = WordNetLemmatizer()
		sent = "The striped bats are hanging on their feet for best"
		cleaned = clean.clean_sentence(sent, lemmatizer = lemmatizer)
		assert cleaned == "the striped bat be hang on their foot for best"

	def test_lower(self):
		# tests whether function keeps casing of original text when desired
		clean = CleanText("", lower = False, special_characters = False)
		sent = "The Code was BEING so ANnoying today....!!!!"
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "The Code was BEING so ANnoying today....!!!!"


	#################################################################################################################
	# NOTE: the following tests cannot be commited to GitHub as the SSA dataset and gv_raw dataset is not uploaded  #
	# PLEASE uncomment when you are testing on your device as this is an important part of the code					#
	#################################################################################################################

	'''
	def test_ssa1(self):
		# tests whether names are properly converted to genders
		clean = CleanText("", gender_ssa_file="/project2/adukia/miie/visualizations/supplemental/data/SSA_names.csv")
		sent = "her name was Sophia and she was an amazing person and was friends with Alice who liked Jim."
		nlp = clean.generate_spacy_params()
		cleaned = clean.clean_sentence(sent, nlp = nlp)
		assert cleaned == "her name was female and she was an amazing person and was friends with female who liked male."

	def test_categorize9(self):
		# checks character classification of entity with first and last name
		clean = CleanText("", gender_ssa_file="/project2/adukia/miie/visualizations/supplemental/data/SSA_names.csv", lower=True)
		sentence = "I wonder what Susie Smith was doing right now she must be painting"
		nlp = clean.generate_spacy_params()
		cleaned = clean.clean_sentence(sentence, nlp = nlp)
		assert cleaned == "i wonder what female was doing right now she must be painting"

	def test_categorize10(self):
		# checks famous classification of an entity
		clean = CleanText("", categorize_famous_file="/project2/adukia/miie/text_analysis/supplemental_data/Categories/", categorize_famous_subcats=["black_female", "black_male"], lower=True)
		sentence = "Rosa Parks's is one of the most powerful women"
		nlp = clean.generate_spacy_params()
		cleaned = clean.clean_sentence(sentence, nlp = nlp)
		assert cleaned == "black_female is one of the most powerful women"

	def test_categorize11(self):
		# checks classification of words with dashes
		clean = CleanText("", categorize_domain_file = "/project2/adukia/miie/text_analysis/supplemental_data/Categories/", categorize_domain_subcats=["wealth", "male_words"], lower=False, special_characters= True)
		sentence = "He was very well-to-do and definitely upper-class"
		cleaned = clean.clean_sentence(sentence)
		assert cleaned == "male_words was very wealth and definitely wealth"

	def test_case_sensitive(self):
		# tests whether case sensitive categorization works
		clean = CleanText("", lower = False, special_characters = True, categorize_domain_file = "/project2/adukia/miie/text_analysis/supplemental_data/Categories/", categorize_domain_subcats = ["power", "appearance"], case_sensitive = True)
		sent = "She was pretty and worked in the Cabinet. The cabinet was small and needed DEMOCRACY!"
		cleaned = clean.clean_sentence(sent)
		assert cleaned == "She was appearance and worked in the power The cabinet was small and needed power"

	def test_categorize9(self):
		# checks character classification of entity with first and last name
		clean = CleanText("", gender_ssa_file="/project2/adukia/miie/visualizations/supplemental/data/SSA_names.csv", lower=True, special_characters=True, stopwords_add=['s'])
		sentence = "I wonder what Susie's group was doing right now she must be painting"
		cleaned = clean.clean_sentence(sentence, nlp = clean.generate_spacy_params())
		assert cleaned == "i wonder what female group was doing right now she must be painting" 
	'''

