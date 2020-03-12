from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
import os
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

STOP_WORDS = set(stopwords.words('english'))

def removeUnsuitableStringsFromList(l: list, stop_words:set= STOP_WORDS) -> (list, list):
  new_tokens = []; unwanted_tokens = []
  for s in l:
    if s.isnumeric() or s in string.punctuation: unwanted_tokens.append(s); continue # check if is numeric or punctuation (_#. ...)
    if re.search(r'[~=]', s) or re.search(r'^[’“”…]|[\.]+$', s): unwanted_tokens.append(s); continue # search for strange occurenes
    if re.search(r'[\d]+[a-z]+', s): unwanted_tokens.append(s); continue # remove the uuid-like strings
    m = re.search(r'^.*?([\w]+).*?$', s) # remove points from around
    s = m.group(1)
    if s in stop_words: unwanted_tokens.append(s); continue # check if it's in stop words
    new_tokens.append(s)
  return new_tokens, unwanted_tokens

def getFilteredTokensFromString(s:str, stop_words:set=STOP_WORDS) -> list:
  word_tokens = word_tokenize(s)
  return removeUnsuitableStringsFromList(word_tokens, stop_words)

def getGloveModel(dim_n:int=300):
  glove_input_file = f'../models/glove.6B.{dim_n}d.txt'
  word2vec_output_file = f'../models/glove.6B.{dim_n}d.txt.word2vec'
  glove_input_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), glove_input_file))
  word2vec_output_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), word2vec_output_file))
  if not os.path.isfile(word2vec_output_file): glove2word2vec(glove_input_file, word2vec_output_file)
  return KeyedVectors.load_word2vec_format(word2vec_output_file, binary=False)

