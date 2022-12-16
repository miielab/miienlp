#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert a model.bin from word2vec to a csv file.

"""

from gensim.models.keyedvectors import KeyedVectors


input_path = '/location/of/model.bin'

# specify the output path and add "model.csv" as your output 
output_path = '/location/of/model.csv'

model = KeyedVectors.load_word2vec_format(input_path, binary=True)
model.save_word2vec_format(output_path, binary=False)