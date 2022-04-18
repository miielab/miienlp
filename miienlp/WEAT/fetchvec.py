import numpy as np
import sys, os, pickle
import wordtest
import utils
import gensim

class FetchVec:
    def __init__(self, model_dir, out_dir, test_dir,
                 vocab_filetype, model_filetype):
        self.out_dir = out_dir + '/TEMP'
        self.model_dir = model_dir
        self.test_dir = test_dir
        self.vocab_filetype = vocab_filetype
        self.model_filetype = model_filetype
        self.vfns = [] # List of files containing vocab
        self.wfns = [] # List of files containing word embeddings

        if not self.vocab_filetype:
            self.vocab_filetype = ".txt"
        #elif vocab_filetype[0] != '.':
        #    self.vocab_filetype = '.' + vocab_filetype
        if not self.model_filetype:
            self.model_filetype = ".bin"
        #elif vocab_filetype[0] != '.':
        #    self.model_filetype = '.' + model_filetype

    def locate_model_files(self):
        if self.model_filetype != ".bin":
            self.vfns = os.listdir(self.model_dir)
            self.vfns = [fn for fn in self.vfns if (fn.endswith(self.vocab_filetype) and fn[:-4]!='log')]

            self.wfns = os.listdir(self.model_dir)
            self.wfns = [fn for fn in self.wfns if fn.endswith(self.model_filetype)]

            if len(self.vfns)!=len(self.wfns):
                raise ValueError('Weight and Vocab does not match.')
                print(self.model_dir)
        else:
            self.wfns = os.listdir(self.model_dir)
            self.wfns = [fn for fn in self.wfns if fn.endswith(self.model_filetype)]

    def load_vocab_file(self, vfn):
        '''
        Load vocabulary file according to file type
        '''
        vocab = None

        if self.vocab_filetype == '-vocab.pkl':
            vocab = np.load(self.model_dir + '/' + vfn, allow_pickle = True)
        elif self.vocab_filetype == '.txt':
            with open(self.model_dir + '/' + vfn,'r') as f:
                vocab = f.read().split('\n')
        else:
            print("Fetchvec doesn't support this vocab filetype yet: " + self.vocab_filetype)

        return vocab

    def load_weights_file(self, wfn):
        '''
        Load the weights (word embeddings) file according to filetype
        '''
        weights = None

        if self.model_filetype == '.npy' or self.model_filetype == '-w.npy':
            weights = np.load(self.model_dir + '/' + wfn)
        else:
            print("Fetchvec doesn't support this weights filetype yet: " + self.model_filetype)
        return weights

    def fetch_vectors(self):
        '''
        Fetches the embedding vectors for a vocabulary list for each
        embedding vector file.
        '''
        outdir_model = self.out_dir + '/' + 'models'
        vocab_dir = self.out_dir + '/' + 'vocab.txt'

        if not os.path.isdir(self.out_dir):
            # Generates output dir if doesn't exist
            os.mkdir(self.out_dir)

        if not os.path.isfile(vocab_dir):
	    # Generates vocab.txt (with the vocabulary)
            utils.load_test_batch(self.test_dir, self.out_dir)

        if not os.path.isdir(outdir_model):
            # Generates folder for output models
            os.mkdir(outdir_model)

        # Locate the vector + vocab files
        self.locate_model_files()

        # Read the custom vocabulary list
        with open(vocab_dir,'r') as f:
            wlist = f.read()
        wlist = wlist.split('\n')

        if self.model_filetype != ".bin":
            # Save custom vector files for each input model file
            for i in range(len(self.vfns)):
                custom_weights = []

                # Load a single pair of vocab and word embedding files
                vfn = self.vfns[i]
                wfn = vfn[:-(len(self.vocab_filetype))] + self.model_filetype
                vocab = self.load_vocab_file(vfn)
                weights = self.load_weights_file(wfn)

                model = {}

    	    # Map vocab-weights into a dictionary
                for i,word in enumerate(vocab):
                    try:
                        model[word] = weights[i]
                    except:
                        print(vfn)
                        print(wfn)
                        print('Model not in correct format!')
                        break

                dim = weights.shape[1]
                unk = np.zeros(dim,dtype=float)

    	    # Add our custom weights to matrix
                for word in wlist:
                    if word not in vocab:
                        custom_weights.append(list(unk))
                    else:
                        custom_weights.append(list(model[word]))

                mat = np.matrix(custom_weights)
                mat.dump(outdir_model + '/' + wfn)
                print(wfn + ' is processed.')
        else:
            for i in range(len(self.wfns)):
                # Load in the model
                custom_weights = []
                model = gensim.models.KeyedVectors.load_word2vec_format(self.model_dir + '/' + self.wfns[i], binary=True)

                dim = model.vector_size
                unk = np.zeros(dim,dtype=float)

    	    # Add our custom weights to matrix
                for word in wlist:
                    if word not in model:
                        custom_weights.append(list(unk))
                    else:
                        custom_weights.append(list(model[word]))

                mat = np.matrix(custom_weights)
                mat.dump(outdir_model + '/' + self.wfns[i].replace(".bin", ".npy"))
                print(self.wfns[i] + ' is processed.')

        print('Fetchvec done!')
        return
