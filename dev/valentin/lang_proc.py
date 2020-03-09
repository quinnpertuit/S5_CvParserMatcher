from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
from pprint import pprint as pp

STOP_WORDS = set(stopwords.words('english'))

def removeUnsuitableStringsFromList(l: list, stop_words:set= STOP_WORDS) -> (list, list):
  new_tokens = []; unwanted_tokens = []
  for s in l:
    if s.isnumeric() or s in string.punctuation: unwanted_tokens.append(s); continue # check if is numeric or punctuation (_#. ...)
    if re.search(r'[~=]', s) or re.search(r'^[’“”…]|[\.]+$', s): unwanted_tokens.append(s); continue # search for strange occurenes
    if re.search(r'[\d]+[a-z]+', s): unwanted_tokens.append(s); continue # remove the uuid-like strings
    #print(s)
    m = re.search(r'^.*?([\w]+).*?$', s) # remove points from around
    s = m.group(1)
    if s in stop_words: unwanted_tokens.append(s); continue # check if it's in stop words
    new_tokens.append(s)
  return new_tokens, unwanted_tokens

def getFilteredTokensFromString(s:str, stop_words:set=STOP_WORDS) -> list:
  word_tokens = word_tokenize(s)
  return removeUnsuitableStringsFromList(word_tokens, stop_words)