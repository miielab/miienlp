import pytest, sys
import os.path
sys.path.insert(0, '../../miienlp/weat')
from wordtest import Single_WordTest, T1, T2

parameters =\
{'run_analysis': "t",
'run_cleaning': "",
'model_directory': "../../examples/test_data/",
'output_directory' : "../../examples/test_data/",
'output_file' : "../../examples/test_data/weat_output_file.json",
'test_directory': "../../examples/test_data/",
'vocabulary_suffix': "npy",
'embeddings_suffix': "txt",
'reuse_fetchvec': "t",
'clean_csv': "",
'clean_out': ""}


class TestWEAT(object):

  def test_output(self):
        # tests output filename creation
        weat_scores = T1()
        weat_scores.single_full_test()
        
        assert os.path.exists('../../examples/test_data/weat_output_file.json')
