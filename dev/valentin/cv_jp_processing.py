import networkx as nx
from gensim.models import KeyedVectors
import graph_treat as gt
import helpers as hp
import lang_proc as lp

def stringToCultureGraph(G: nx.DiGraph, w2vec_model:KeyedVectors, s:str, debug=False):
  filtered_tokens, _ = lp.getFilteredTokensFromString(s)
  culture_terms = gt.getLeavesFromGraphImposingDistanceFromOrigin(G, 6)
  to_study_terms, to_study_not_found = hp.getItemsContainedInListAndNot(filtered_tokens, w2vec_model.wv.vocab)
  culture_terms, culture_not_found = hp.getItemsContainedInListAndNot(culture_terms, w2vec_model.wv.vocab)
  gt.calculateAllSimilaritiesFromListWithGraph(G, w2vec_model, to_study_terms, culture_terms, debug=debug)
  return to_study_not_found, culture_not_found