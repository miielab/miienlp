import pytest, sys
import os.path
sys.path.insert(0, '../../miienlp/embeddings')
from word_vecs import WordVectors
#from data_prep import WVecDataPreparation

model =\
{"name": "word2vec",
  "size": 300,
  "num_models": 3,
  "window": 5,
  "min_count": 10,
  "workers": 5,
  "sg": 1,
  "hs": 1,
  "negative": 0,
  "epochs":5
  }

output =\
{"output_model_dir": "../../unittest/wordEmbeddings/test_data/",
 "save_vocab_np": True,
 "save_vocab_txt": True
}

data_dir= "../../unittest/wordEmbeddings/test_data/1992_tx_m_5_0021084963_s.txt"

class TestWordEmbedding(object):
  '''  
  def test_combine_text(self):
        dp = WVecDataPreparation(data_dir, time_series, collection_corpora)
        time_frame = dp.construct_time_series()
        df = dp.construct_relevant_file_path_df(time_frame)
        comb_path = dp.combine_text(df)
        assert df.head() == ["time_series"]
  '''
  def test_output(self):
        # tests output filename creation
        #word_vect = WordVectors(data_dir, model, output, '')
        #w2v_file = word_vect.make_w2v_model()
        #assert output_file == "../../examples/test_data/model_0.bin"
        wemb = WordVectors(data_dir, model, output, 0)
        wemb.make_w2v_model()
        
        assert os.path.exists('../../unittest/wordEmbeddings/test_data/model_0.bin')
        
