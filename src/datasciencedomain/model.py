import pickle
import os
import json

from datasciencedomain.config import Config


class Model:
    """ A simple abstraction layer for using the Word Embedding Model """
    
    def __init__(self, load_model = True):
        """ Initialising the model class
        """
        self.model = dict()
        self.config = Config()
        if load_model:
            self.load_chached_model()

        
    def check_word_in_model(self, word):
        """ It checks whether a word is available in the model
        """
        if word in self.model:
            return True
        
        return False


    def get_words_from_model(self, word):
        """ Returns the similar words to the word:word
        Args:
            word (string): word that potentially belongs to the model
        
        Return:
            dictionary: containing info about the most similar words to word. Empty if the word is not in the model.
        """
        try:
            return self.model[word]
        except KeyError:
            return {}


    def load_chached_model(self):
        """Function that loads the cached Word2vec model. 
        The ontology file has been serialised with Pickle. 
        The cached model is a json file (dictionary) containing all words in the corpus vocabulary with the corresponding CSO topics.
        The latter has been created to speed up the process of retrieving CSO topics given a token in the metadata
        """
        
        with open(self.config.get_cached_model()) as f:
           self.model = json.load(f)
        print("Model loaded.")
           
    
      
# =============================================================================
#         LEGACY CODE: just in case we want to use the model as is
# =============================================================================
            
    def load_model(self):
        """Function that loads Word2vec model. 
        This file has been serialised using Pickle allowing to be loaded quickly.
        """
        self.check_model()
        self.model = pickle.load(open(self.config.get_model_pickle_path(), "rb"))
    


