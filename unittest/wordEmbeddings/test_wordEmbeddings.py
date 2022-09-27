import pytest, sys
sys.path.insert(0, '../../miienlp/embeddings')
from word_vecs import WordVectors
from data_prep import WVecDataPreparation

time_series =\
{"type": "decade",
 "time_frame": "all"
}

model =\
{"name": "word2vec",
  "size": 300,
  "window": 5,
  "min_count": 20,
  "workers": 5,
  "sg": 1,
  "hs": 1,
  "negative": 0,
  "epochs":5
  }
output =\
{"output_model_dir": "test_results",
 "save_vocab_np": True,
 "save_vocab_txt": True
}

collection_corpora =\
{"mainstream":["caldecott", "newbery"]
}

data_dir= "test_data/"

class TestWordEmbedding(object):
    def test_combine_text(self):
        dp = WVecDataPreparation(data_dir, time_series, collection_corpora)
        time_frame = dp.construct_time_series()
        df = dp.construct_relevant_file_path_df(time_frame)
        comb_path = dp.combine_text(df)
        assert df.head() == ["time_series"]
