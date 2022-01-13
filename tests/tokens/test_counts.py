import pytest, sys
#sys.path.insert(0, 'miienlp/tokens/')
from collections import Counter
from miienlp.tokens.utils import load_data
from miienlp.tokens.counts import Counts


class TestCounts(object):

    def test_counts1(self):
        # tests categories are extracted correctly and obey the "type" parameter (upper/lower or upper or lower)
        wc = Counts("", "/project2/adukia/miie/text_analysis/supplemental_data/Categories/", ['black_words'], "spacy", _type='LU')
        assert sorted(wc.categories['black_words']) == sorted(["black", "blacks", "Black", "Blacks"])
    
    def test_counts2(self):
        # tests specical case of pronouns (i.e. ignore type LU and just do lower or upper)
        wc = Counts("", "/project2/adukia/miie/text_analysis/supplemental_data/Categories/", ['male_pronouns_lower'], "spacy", _type='LU')
        assert sorted(wc.categories['male_pronouns_lower']) == sorted(["he", "him", "himself", "his", "hisself"])
    
    def test_counts3(self):
        # tests specical case of pronouns (i.e. ignore type LU and just do lower or upper)
        wc = Counts("", "/project2/adukia/miie/text_analysis/supplemental_data/Categories/", ['female_pronouns_upper'], "nltk", _type='LU')
        assert sorted(wc.categories['female_pronouns_upper']) == sorted(["She", "Her", "Herself", "Hers"])

    def test_counts4(self):
        # tests specific word frequency using spacy
        data = "Michelle was a girl. Her mother was a woman who loved her hair. Tom was a boy who loved his Grandfather and dog."
        wc = Counts(data, "/project2/adukia/miie/text_analysis/supplemental_data/Categories/", ['female', 'male', 'appearance', 'animal'], "spacy", _type='LU')
        spacy_txt = wc.generate_spacy_data()
        counts = wc.count_freq_spacy(spacy_txt)
        assert counts == {'female': 5, 'male': 3, 'appearance': 1, 'animal': 1}

    def test_counts5(self):
        # tests specific word frequency using nltk
        data = "She was a black woman with blacks and blacks and White"
        wc = Counts(data, "/project2/adukia/miie/text_analysis/supplemental_data/Categories/", ['black_words', 'white_words'], method="nltk", _type='LU')
        counts = wc.count_freq_nltk()
        assert counts == {'black_words': 3, "white_words":1}

    def test_counts6(self):
        # tests nltk proportion counter
        data = "She was a black woman with blacks and blacks and White"
        wc = Counts(data, "/project2/adukia/miie/text_analysis/supplemental_data/Categories/", ['black_words', 'white_words'], method="nltk", _type='L')
        counts, spec_counts = wc.count_prop_nltk()
        assert spec_counts == {'black_words':{'black': 1, 'blacks':2}, 'white_words':{'white': 1, 'whites': 0}}
