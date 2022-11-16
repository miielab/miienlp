import pytest, sys
import os.path
sys.path.insert(0, '../../miienlp/weat')
from wordtest import Single_WordTest, T1, T2, Multiple_WordTests
from fetchvec import FetchVec

params =\
{'run_analysis': "t",
'run_cleaning': "",
'model_directory': "../../examples/test_data/",
'output_directory' : "../../examples/test_data/",
'output_file' : "../../examples/test_data/weat_output_file.json",
'test_directory': "../../examples/test_data/json_weat/",
'vocabulary_suffix': "npy",
'embeddings_suffix': "txt",
'reuse_fetchvec': "t",
'clean_csv': "",
'clean_out': ""}


class TestWEAT(object):

  def test_output(self):
      fv = FetchVec(params["model_directory"],
                          params["output_directory"],
                          params["test_directory"],
                          params["vocabulary_suffix"],
                          params["embeddings_suffix"])
      fv.fetch_vectors()

      wt = Single_WordTest(params["test_directory"],
                           params["output_directory"],
                           params["output_file"])

      # tests output filename creation
      weat_scores = T1() #curr_test -- 3 embed, curr_model
      weat_scores.single_full_test()

      assert os.path.exists('../../examples/test_data/weat_output_file.json')
