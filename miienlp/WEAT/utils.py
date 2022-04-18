'''
Built from utils.py in MiiE Text Cleaning repository.
'''

import yaml
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json, sys, os

_curdir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARAMS_FILE = os.path.join(_curdir, 'input.yaml')

def get_params(params_file=DEFAULT_PARAMS_FILE, args=None):
    with open(params_file, 'r') as stream:
        params = yaml.safe_load(stream)
    params = check_dir_params(params)
    return params

def check_dir_params(params):
    check_dirs = ["model_directory", "test_directory"]
    for directory in check_dirs:
        params[directory] = validate_data_dir(params[directory])
    return params

def validate_data_dir(data_dir):
    '''
    Checks whether the data directory is valid
    '''
    if os.path.isdir(data_dir):
        return os.path.abspath(data_dir)
    else:
        raise Exception("The directory located at", data_dir, "does not exist. Please specify valid path.")

############################################################
#### Loading the tests and vocabulary ######################
############################################################

### Data Loader 
def load_test(fn):
    with open(fn,'r') as f:
        dat = json.load(f)
    if "test" not in dat: 
        print("Test lists missing!")
    elif "gender" not in dat:
        print("Gender lists missing!")
    elif len(dat["gender"])!=2:
        print("Invalid gender lists!")
    elif len(dat['test'])>2:
        print("Too many test lists!")
    elif len(dat['test'])<1:
        print("No test list!")
    else:
        test_type = 'T'+str(len(dat['test']))
        test_cate = ','.join(list(dat['test']))
        print('Bias test of type '+test_type+' on '+test_cate+' is loaded.')
        return dat, len(dat['test'])
    return {}, -1

def load_test_vocab(fn):
    with open(fn, 'r') as f:
        vocab = f.read()
        vocab = vocab.split()
    return vocab

def load_test_batch(Testdir = 'tests', Vocab = None):
    res = {}
    fns = os.listdir(Testdir)
    fns = [fn for fn in fns if fn.endswith('json')]
    co = 0
    v = []
    for fn in fns:
        dat, typ = load_test(os.path.join(Testdir,fn))
        if typ > 0:
            co += 1
            for vt in dat['test']:
                if len(dat['test'][vt]):
                    dat['test'][vt] = load_test_vocab(dat['test'][vt][0])
                    v += dat['test'][vt]
            for vg in dat['gender']:
                if len(dat['gender'][vg]):
                    dat['gender'][vg] = load_test_vocab(dat['gender'][vg][0])
                    v += dat['gender'][vg]
            res[fn[:-5]] = {'wordlists':dat,'type':typ}

    v = sorted(list(set(v)))
    if not Vocab==None:
        print(Vocab)
        with open(Vocab +'/'+ 'vocab.txt','w+') as f:
            f.write('\n'.join(v))
        print('Required vocabulary created in vocab.txt.')
    print('Successfully loaded %d tests!'%(co))
    return res

def load_model_batch(Modeldir='vec'):
    res = {}
    md = os.listdir(Modeldir)
    mfns = [fn for fn in md if fn.endswith('.npy')]
    c = 0
    for m in mfns:
        res[m[:-4]] = np.load(os.path.join(Modeldir,m),allow_pickle=True)
        print('Model loaded: '+m)
        c+=1
    print('Successfully loaded %d models!'%(c))
    return res

        ############################################################
    #### Computing the values to output to the tests ###########
    ############################################################

def cosim(V1, V2):
    '''
    Calculates cosine similarity between two embeddings.
    Currently uses library function based off of Jones paper.
    Specific cosine similarity implementation is wrapped in this cosim()
    so that the implementation can be changed as necessary.

    Input:
    -- V1: vocab word 1 (as an embedding vector)
    -- V2: vocab word 2 (as an embedding vector)

    Return:
    -- cosine similarity btwn two words (embeddings).
    '''
    return cosine_similarity(V1, V2)[0][0]

def cosim_batch(g1, g2):
    '''
    Input:
    -- G1:List of embedding vectors for a group of words,
           such as career words
    -- G2: List of embedding vectors for the words in
            a second group of words, like female words

    Return:
    -- List of cosine similarity for each pair of words
        in the two groups (or between a domain and a group). 
    '''
    simlist = []
    for v1 in g1:
        for v2 in g2:
            simlist.append(cosim(v1,v2))
    return np.array([simlist])

def diff_cosim(v1, g1, g2):
    '''
    Used in T2
    '''
    cos1 = []
    cos2 = []
    for g in g1:
        cos1.append(cosim(v1,g))
    for g in g2:
        cos2.append(cosim(v1,g))
    return np.mean(cos1) - np.mean(cos2)

def diff_cosim_batch(g1, g2, g3):
    '''
    Used in T2
    '''
    return [diff_cosim(g,g2,g3) for g in g1]

def normalized_cosim(a1, a2):
    '''
    Get the mean of the cosine similarity for
    the two lists of cosine similarity. 
    '''
    return np.mean(a1), np.mean(a2)

def jones_bias(a1, a2):
    return np.mean(a2) - np.mean(a1)

def sample_permutation(l,B=500):
    res = []
    half = l/2
    for b in range(B):
        arr = np.random.permutation(l)
        res.append([list(arr[:int(half)]),list(arr[int(half):])])
    return res

def permute(v,p):
    if len(p)>len(v):
        print(p)
        print(v)
        raise ValueError('Invalid permutation')
    else:
        return [v[i] for i in p]

def not_unk(vec):
    test_vec = np.zeros(vec.shape[0],dtype=float)
    res = np.sum(test_vec==np.array(vec))
    if res==0:
        return True
    else:
        return False

