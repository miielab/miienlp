import numpy as np
import json, sys, os
import utils
import statsmodels.api as sm

    
############################################################
#### Evaluating all the tests in the given folder    #######
############################################################

class Multiple_WordTests():
    def __init__(self, test_dir, out_dir, out_file):
        self.test_dir = test_dir
        self.out_dir = out_dir
        self.out_file = out_file
        self.tests = None
        self.models = None
        self.w2i = None
        self.test_results = {}

    def make_single_test(self, test_type, curr_model, curr_test):
        '''
        Directs program to the correct test,
        based off the test id. 

        Input:
        -- Test: Three lists of embedding vectors. Each list is the embedding vectors for
        all the words in a group (e.g. one list contains the vectors representing words in 'male')
        -- Embedding: embeddings
        -- id: Test id
        
        '''
        if test_type == 1:
            return T1(curr_test, curr_model, self.w2i)
        elif test_type == 2:
            return T2(curr_test, curr_model, self.w2i)
        else:
            raise ValueError('Invalid test type: ' + str(id))
        return

    def batch_test(self):
        '''
        Runs all WEAT tests and save each test result to its own JSON file 
        '''
        try:
            with open(self.out_dir + '/TEMP/vocab.txt') as f:
                vocab = f.read().split('\n')
            self.w2i = {w:i for i,w in enumerate(vocab)}
            EXIST_VOCAB = 1
        except:
            EXIST_VOCAB = 0
            vocab = None

        self.tests = utils.load_test_batch(self.test_dir, self.out_dir + '/TEMP')
        temp_models_dir = self.out_dir + "/TEMP/models"
        self.models = utils.load_model_batch(temp_models_dir)

        for t in self.tests:
            self.test_results[t] = {}

            print('Evaluating test ' + t)
            for m in self.models:
                print('Testing model ' + m)

                single_wordtest = self.make_single_test(self.tests[t]['type'],
                                                   self.models[m],
                                                   self.tests[t]['wordlists'])

                # assoc1 = male association, assoc2 = female assocation
                # bias = assoc2 - assoc1 
                assoc1, assoc2, bias, abs_bias, ep, stats = single_wordtest.single_full_test()

                t_stat, pvalue, n1, n2 = stats
                
                try:
                    self.test_results[t][m] = {'M_Assoc':float(assoc1),
                                               'F_Assoc':float(assoc2),
                                               'Abs_Bias': float(abs_bias),
                                               'Bias': float(bias),
                                               'EWP': float(ep),
                                               'P_value': float(pvalue),
                                               'T_statistic': float(t_stat),
                                               'N1': float(n1),
                                               'N2': float(n2)}
                except:
                    self.test_results[t][m] = {'M_Assoc':'N/A',
                                               'F_Assoc':'N/A',
                                               'Abs_Bias': 'N/A',
                                               'Bias':'N/A',
                                               'EWP': float(ep),
                                               'Pval': 'N/A',
                                               'T_statistic': 'N/A',
                                               'N1': 'N/A',
                                               'N2': 'N/A'}
                    
        with open(self.out_file, 'w+') as f:
            json.dump(self.test_results, f, indent=12)
            
        print('All tests and models are evaluated.')
        return

class Single_WordTest:
    def __init__(self, curr_test, curr_model, w2i):
        self.curr_test = curr_test
        self.curr_model = curr_model
        self.w2i = w2i

    def calculate_ewp(self, m):
        '''
        Calculate Effective Word Percentage (EWP), i.e.
        percentage of all the words used in this test
        that had valid corresponding embedding vectors 

        Input:
        --m: List of structures of the form (wordlist valid length, wordlist full length),
        for each wordlist used in this test. The valid length is the number
        of valid vectors found for that wordlist; full length is the 
        number of words in the wordlists. 

        Output:
        -- EWP
        '''
        ewp_m = np.sum(m.T, axis = 1)
        return ewp_m[0] / ewp_m[1]

    def list2idx(self, word_list):
        '''
        Given a list of vocab words, convert each word
        to its respective index (which refer to a word embedding vector)

        Input:
        --word_list: List of vocab word strings

        Output:
        --list of indices that correspond to the word list
        '''
        return [self.w2i[w] for w in word_list]

    def idx2vec(self, idx_list):
        '''
        Given a list of indices (corresponding to a vocab word),
        convert each index to a word embedding vector. Checks
        that the vector is valid before adding it to the final
        output list. 

        Input:
        --idx_list: list of indices

        Output:
        --list of word embedding vectors corresponding to the indices
        '''
        res = []
        for i in idx_list:
            v = self.curr_model[i]
            if utils.not_unk(v):
                res.append(v)
        return res

    def list2vec(self, wordlists):
        '''
        Convert one or more lists of words into a list of
        word embedding vectors that refer to those words.

        Input:
        --wordlists: one or more lists of words (represented as strings)

        Output:
        --res: one or more lists of word embedding vectors
        --EWP: total percentage of words that had valid vectors across
               all the wordlists 
        '''
        res = []
        res_meta = []
        for wlist in wordlists:
            ilist = self.list2idx(wlist)
            vlist = self.idx2vec(ilist)
            full_length = len(ilist)
            valid_length = len(vlist)
            res.append(vlist)
            res_meta.append([valid_length, full_length])
        return res, self.calculate_ewp(np.array(res_meta, dtype=float))

    def test_not_valid(self, aar):
        '''
        Check validity of test.

        Input:
        --aar: Array containing list of group 1 vectors, list of group 2 vectors,
               and list of domain vectors

        Output:
        -- True if any of the three lists are empty. False otherwise.
        '''
        res = False
        for l in aar:
            if len(l) == 0:
                res = True
        return res


############################################################
#### T1 Test: Comparing 1 domain with 2 groups    ##########
############################################################

class T1(Single_WordTest):
    
    def T1_load(self):
        '''
        Input:
        -- Test: raw test data
        -- Embedding: embeddings

        Output:
        -- vector lists
        '''
        c1 = list(self.curr_test['test'])[0]
        wordlists = [self.curr_test['gender']['male'],
                     self.curr_test['gender']['female'],
                     self.curr_test['test'][c1]]
        
        return self.list2vec(wordlists)

    def T1_stats(self, L1, L2):
        '''
        Calculates relevant statistics for T1 test.

        Input:
        --L1: list of pairwise cosine similarities between group 1 and domain
        --L2: list of pairwise cosine similarities between group 2 and domain

        Output:
        -- t-statistic and p-value
        '''
        X = np.concatenate((L1, L2), axis = 1)
        X = X.T
        Y = np.array([0] * L1.size + [1] * L2.size) # 0: male, 1: female
        logit_model=sm.Logit(Y,X)
        result=logit_model.fit()
        pval = result.pvalues[0]
        Tstat = result.tvalues[0]
        return Tstat, pval

    def T1_test(self):
        '''
        Runs T1 test (2 groups vs 1 domain. Associations
        calculated between group 1 vs domain and group 2 vs domain)

        Input:
        -- Test: Three lists of embedding vectors. Each list is the embedding vectors for
        all the words in a group (e.g. one list contains the vectors representing words in 'male')

        Output:
        --assoc1: association (male)
        --assoc2: association (female)
        --bias: assoc1 - assoc2
        --abs_bias: absolute value of bias
        --stats: t-statistic, p-value, n1, n2
        '''
        group1_vecs, group2_vecs, domain_vecs = self.curr_test
        
        if self.test_not_valid([group1_vecs, group2_vecs, domain_vecs]):
            return -2,-2,-2,-2, [-2, -2, -2, -2]
        else:
            group1_dom_pairs = utils.cosim_batch(group1_vecs, domain_vecs)
            group2_dom_pairs = utils.cosim_batch(group2_vecs, domain_vecs)
            t_stat, pvalue = self.T1_stats(group1_dom_pairs, group2_dom_pairs)
            assoc1, assoc2 = utils.normalized_cosim(group1_dom_pairs, group2_dom_pairs)
            bias = utils.jones_bias(group1_dom_pairs, group2_dom_pairs)
            abs_bias = abs(bias)
            stats = [t_stat, pvalue, group1_dom_pairs.size, group2_dom_pairs.size]
            return assoc1, assoc2, bias, abs_bias, stats

    def single_full_test(self):
        '''
        Runs a test (i.e. get the associations
        and biases) between a group and a domain,
        for two groups.

        Input:
        --Test
        --Embedding

        Output:
        --assoc1: association (male)
        --assoc2: association (female)
        --bias: assoc1 - assoc2
        --abs_bias: absolute value of bias
        --ep: effective word percentage, i.e.
            how many of the vocab words had
            valid vectors that could be used in
            calculating the T1 test scores
        --stats: t-statistic, p-value, n1, n2
        '''
        cleaned_test, ep = self.T1_load()
        self.curr_test = cleaned_test
        assoc1, assoc2, bias, abs_bias, stats = self.T1_test()

        return assoc1, assoc2, bias, abs_bias, ep, stats

############################################################
#### T2 Test: Comparing 2 domain with 2 groups    ##########
############################################################

class T2(Single_WordTest):
        
    def T2_load(Test, Embedding):
        c1 = list(Test['test'])[0]
        c2 = list(Test['test'])[1]
        return list2vec([Test['gender']['male'],
                            Test['gender']['female'],
                            Test['test'][c1],
                            Test['test'][c2]], Embedding)

    def T2_test(Test):
        vg1, vg2, vt1, vt2 = Test
        if test_not_valid([vg1,vg2,vt1,vt2]):
            return -1,-1,-1
        else:
            g1t = utils.diff_cosim_batch(vg1,vt1,vt2)
            g2t = utils.diff_cosim_batch(vg2,vt1,vt2)
            score = utils.normalized_score(g1t,g2t)
        return score

    def T2_pval(Test,S0,Size=4096):
        vg1, vg2, vt1, vt2 = Test
        perm_v = vg1+vg2
        perm_l = len(perm_v)
        if perm_l<2 or len(vt1)==0 or len(vt2)==0:
            return -1
        else:
            ps = utils.sample_permutation(perm_l, Size)
            pos = 0.0
            total = 0.0
            for p in ps:
                pg1, pg2 = utils.permute(perm_v,p[0]), permute(perm_v,p[1])
                s = T2_test([pg1,pg2,vt1,vt2])
                if s!=-1:
                    total += 1
                    pos += (s>S0)
            return pos/total
        return -2

    def single_full_test(self):
        test, ep = self.T2_load(self.curr_test, self.curr_model, self.w2i)
        s0 = T2_test(test)
        pval = T2_pval(test, s0)
        return s0, pval, ep
