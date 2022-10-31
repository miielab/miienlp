import pytest, sys
sys.path.insert(0, '../../miienlp/token/')
from pos_counts import POSCounts
from collections import Counter
from ner import NER
from utils import load_data
from specific_words import SpecificWordCounts


class TestCounts(object):
    def test_ner1(self):
        # tests entity extraction
        data = """Abraham was the nicest man who lived and his best friend was Allison."""
        ner = NER(data, ["PERSON"])
        spacy_txt = ner.generate_spacy_data()
        entities = ner.extract_entities(spacy_txt)
        assert entities == [['Abraham', 'PERSON'], ['Allison', 'PERSON']]

    def test_ner2(self):
        # tests clean entities method
        ner = NER(" ", " ", [])
        entities = [['  Abraham!!', 'PERSON'], ['Allison?', 'PERSON'], ["???.APril", 'DATE'], ['Martin Luther King Jr.,', "PERSON"], ['Notorious B.I.G.', 'PERSON']]
        clean_entities = ner.clean_entities(entities)
        assert clean_entities == [["abraham", 'PERSON'], ["allison", 'PERSON'], ["april", "DATE"], ['martin luther king jr.', "PERSON"], ['notorious b.i.g.', 'PERSON']]

    def test_ner3(self):
        # tests clean entities method
        ner = NER(" ", " ", [])
        entities = [[' - Abraham  4568 !!', 'PERSON'], ['... Allison?123', 'PERSON'], ["--all", 'DATE'], ["176 Shen", "PERSON"], ["/  ", "PERSON"]]
        clean_entities = ner.clean_entities(entities)
        assert clean_entities == [["abraham", 'PERSON'], ["allison", 'PERSON'], ["all", "DATE"], ["shen", "PERSON"]]

    def test_ner4(self):
        # tests case where entity has multiple tags
        ner = NER(" ", ['PERSON'])
        entities = [['april', 'DATE'], ['april', 'PERSON'], ['april', 'DATE'], ['april', 'PERSON']]
        df = ner.construct_df(entities)
        filtered_df = ner.filter_results(df)
        assert filtered_df[filtered_df['entity'] == 'april']['freq'].values[0] == 2 and filtered_df[filtered_df['entity'] == 'april']['modal_tag'].values[0] == 'PERSON'
    def test_specific_words1(self):
        # tests categories are extracted correctly and obey the "type" parameter (upper/lower or upper or lower)
        swc = SpecificWordCounts("", "../../miienlp/word_lists/domain/", ['black_words'], "spacy", _type='LU')
        assert sorted(swc.categories['black_words']) == sorted(["black", "blacks", "Black", "Blacks"])
    
    def test_specific_words2(self):
        # tests specical case of pronouns (i.e. ignore type LU and just do lower or upper)
        swc = SpecificWordCounts("", "../../miienlp/word_lists/group/", ['male_pronouns_lower'], "spacy", _type='LU')
        assert sorted(swc.categories['male_pronouns_lower']) == sorted(["he", "him", "himself", "his", "hisself"])
    
    def test_specific_words3(self):
        # tests specical case of pronouns (i.e. ignore type LU and just do lower or upper)
        swc = SpecificWordCounts("", "../../miienlp/word_lists/group/", ['female_pronouns_upper'], "nltk", _type='LU')
        assert sorted(swc.categories['female_pronouns_upper']) == sorted(["She", "Her", "Herself", "Hers"])
    '''
    def test_specific_words4(self):
        # tests specific word frequency using spacy
        data = "Michelle was a girl. Her mother was a woman who loved her hair. Tom was a boy who loved his Grandfather and dog."
        swc = SpecificWordCounts(data, "../../miienlp/word_lists/domain/", ['female', 'male', 'appearance', 'animal'], "spacy", _type='LU')
        spacy_txt = swc.generate_spacy_data()
        counts = swc.count_freq_spacy(spacy_txt)
        assert counts == {'female_words': 5, 'male_words': 3, 'appearance': 1, 'animal': 1}
    '''
    def test_specific_words5(self):
        # tests specific word frequency using nltk
        data = "She was a black woman with blacks and blacks and White"
        swc = SpecificWordCounts(data, "../../miienlp/word_lists/domain/", ['black_words', 'white_words'], method="nltk", _type='LU')
        counts = swc.count_freq_nltk()
        assert counts == {'black_words': 3, "white_words":1}

    def test_specific_words6(self):
        # tests nltk proportion counter
        data = "She was a black woman with blacks and blacks and White"
        swc = SpecificWordCounts(data, "../../miienlp/word_lists/domain/", ['black_words', 'white_words'], method="nltk", _type='L')
        counts, spec_counts = swc.count_prop_nltk()
        assert spec_counts == {'black_words':{'black': 1, 'blacks':2}, 'white_words':{'white': 1, 'whites': 0}}
    
