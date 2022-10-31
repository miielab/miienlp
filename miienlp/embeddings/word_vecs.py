import warnings, os
warnings.filterwarnings('ignore')
import utils
import gensim
from gensim.models import Word2Vec, KeyedVectors
import numpy as np

class WordVectors(object):
    def __init__(self, combined_data_path, model_hparams, output, model_id):
        self.combined_data_path = combined_data_path # one txt file
        self.model_hparams = model_hparams
        self.output = output
        self.model_id = model_id

    def make_w2v_model(self):
        '''
        Constructs word2vec model and saves the model bin, vocab, and vector files
        '''
        # TO DO: write the model parameters to a file so that we can know the difference between multiple models
        sentences = gensim.models.word2vec.LineSentence(self.combined_data_path)
        # TO DO: add more model parameter options and make configurable
        gen_model = gensim.models.Word2Vec(sentences, size=self.model_hparams["size"], window=self.model_hparams["window"],\
                                            min_count=self.model_hparams["min_count"], workers=self.model_hparams["workers"],\
                                            sg=self.model_hparams["sg"], hs=self.model_hparams["hs"], negative=self.model_hparams["negative"],\
                                            iter=self.model_hparams["epochs"])

        
        #out_file = self.combined_data_path.split('/')[-1][:-4] + '.bin'
        print("input path", self.combined_data_path)
        out_file = "model_" + str(self.model_id) + '.bin'
        print("output path", self.output["output_model_dir"] + out_file)
        utils.construct_output_dir(self.output["output_model_dir"])
        gen_model.wv.save_word2vec_format(self.output["output_model_dir"] + out_file, binary=True)

        #if self.output["save_vocab_np"]: self.save_vocab_vectors(model_dir, model_path, time, collection)
        #if self.output["save_vocab_txt"]: self.save_vocab_text(model_dir, model_path, time, collection)
        if self.output["save_vocab_np"]: self.save_vocab_vectors(self.output["output_model_dir"], out_file)
        if self.output["save_vocab_txt"]: self.save_vocab_text(self.output["output_model_dir"], out_file)
        return

    def save_vocab_vectors(self, model_dir, model_path):
        '''
        Saves word vectors as numpy arrays
        '''
        ex = self.load_model(model_dir + model_path)
        word_vectors = ex.wv.vectors
        np.save(model_dir + model_path[:-4] + '_w2v.npy', word_vectors)
        return
    
    def save_vocab_text(self, model_dir, model_path):
        '''
        Saves raw vocab into text file (one word per line)
        '''
        ex = self.load_model(model_dir + model_path)
        vocab = [ k for k, v in ex.wv.vocab.items()]
        with open(model_dir + model_path[:-4] + '_w2v.txt', "w") as output:
            output.write("\n".join(str(i) for i in vocab))
        output.close()
        return
        
    #def save_vocab_vectors(self, model_dir, model_path, time, collection):
    #    '''
    #    Saves word vectors as numpy arrays
    #    '''
    #    ex = self.load_model(model_path)
    #    word_vectors = ex.wv.vectors
    #    np.save(model_dir + '{}_{}_w2v.npy'.format(time, collection), word_vectors)
    #    return
    
    #def save_vocab_text(self, model_dir, model_path, time, collection):
    #    '''
    #    Saves raw vocab into text file (one word per line)
    #    '''
    #    ex = self.load_model(model_path)
    #    vocab = [ k for k, v in ex.wv.vocab.items()]
    #    with open(model_dir + '{}_{}_w2v.txt'.format(time, collection), "w") as output:
    #        output.write("\n".join(str(i) for i in vocab))
    #    output.close()
    #    return

    def make_bert_model(self, time_series, collection):
        pass

    def load_model(self, file):
        '''
        Loads in the word2vec or BERT model
        '''
        if self.model_hparams["name"] == 'word2vec':
            vector_model = gensim.models.KeyedVectors.load_word2vec_format(file, binary=True)
        else:
            vector_model = KeyedVectors.load(file)
        return vector_model
