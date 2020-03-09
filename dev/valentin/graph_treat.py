from networkx.algorithms import shortest_path
import networkx as nx
from gensim.models import KeyedVectors
from functools import reduce
from typing import Any
import helpers as hp
import json

NODE_DISTANCES = (3,4,5,6) # distance from origin to (main_node, antonym_node=child_of_main, term_nodes, terms=leaves)
ORIGIN_TO_LEAVES_DIST = 6
ORIGIN_NAME = 'culture'

def getLeavesFromGraphImposingDistanceFromOrigin(G: nx.DiGraph, path_lenght_from_main:int=ORIGIN_TO_LEAVES_DIST, origin_name:str=ORIGIN_NAME) -> list:
  leaves = []
  for n in G.nodes:
    #print(f'verify - ({G.in_degree(n)}, {len(nx.algorithms.shortest_paths.generic.shortest_path(G, n, "culture"))}) ({n})')
    if G.in_degree(n) == 0 and len(shortest_path(G, n, origin_name)) == path_lenght_from_main:
      leaves.append(n)
  return leaves

def getNodesFromOriginDistance(G: nx.DiGraph, distance: int = 4, origin_name:str=ORIGIN_NAME) -> list:
  return [ n for n in G.nodes if len(shortest_path(G, n, origin_name)) == distance ]

def getTwoGraphsAttributeInfo(G1:nx.DiGraph, G2:nx.DiGraph, distance:int, attribute:str,
  nodes_distances:(int, int, int, int)=NODE_DISTANCES, origin_name:str=ORIGIN_NAME, debug:bool=False):
  (main_node_dist, antonym_node_dist, term_node_dist, term_dist) = nodes_distances
  dict_antonyms = {}
  antonym_nodes_1 = getNodesFromOriginDistance(G1, antonym_node_dist, origin_name)
  for node in antonym_nodes_1:
    dict_antonyms[node] = [0, 0]
    dict_antonyms[node][0] = G1.nodes[node][attribute]
    dict_antonyms[node][1] = G2.nodes[node][attribute]
  return dict_antonyms

def calculateAllSimilaritiesFromListWithGraph(G:nx.DiGraph, w2vec_model:KeyedVectors, terms:list, available_terms:list, 
  nodes_distances:(int, int, int, int)=NODE_DISTANCES, origin_name:str=ORIGIN_NAME, debug:bool=False):
  """
  Get Similarities between terms given and the terms_of_graph (leaves)
  The similarities are calculated by using word2vec and are directly inserted to the Graph

  ----------
  + nodes_distance: distance from origin to (main_node, antonym_node=child_of_main, term_nodes, terms=leaves)
  + origin_name: root
  """
  (main_node_dist, antonym_node_dist, term_node_dist, term_dist) = nodes_distances
  main_nodes = getNodesFromOriginDistance(G, main_node_dist, origin_name)
  for main_node in main_nodes:
    [left_antonym, right_antonym] = list(G.predecessors(main_node))
    left_similarities = getSimilarities(G, w2vec_model, left_antonym, terms, available_terms, debug=debug)
    if debug: print('----------')
    right_similarities = getSimilarities(G, w2vec_model, right_antonym, terms, available_terms, debug=debug)
    left_sim_mean = hp.calculateMeanOfListOfTuples(left_similarities, 1)
    right_sim_mean = hp.calculateMeanOfListOfTuples(right_similarities, 1)
    if debug: print(f'({left_antonym}, {round(left_sim_mean*100, 2)}%) { ">" if left_sim_mean > right_sim_mean else "<" } ({right_antonym}, {round(right_sim_mean*100,2)} %)')
    if debug: print('========================')
    addAntonymAttribute(G, 'similarity', (left_antonym, right_antonym), (left_sim_mean, right_sim_mean))

def getSimilarities(G: nx.DiGraph, w2vec_model: KeyedVectors, term_nodes: list, terms: list, available_terms: list, debug:bool=False):
  similarities = []
  for term_node in G.predecessors(term_nodes):
    term_leaves = list(G.predecessors(term_node))
    term_leaves = [ term for term in term_leaves if term in available_terms ]
    if len(term_leaves) == 0: continue
    similarity = w2vec_model.n_similarity(term_leaves, terms) 
    similarities.append((term_node, similarity))
    if debug: print(f'({term_node}, {similarity})')
  return similarities

def addAntonymInfo(G: nx.DiGraph, left_right: (str, str), left_right_terms: (list, list)) -> None:
  G.add_edges_from( [ (sub, left_right[0]) for sub in left_right_terms[0] ])
  G.add_edges_from( [ (sub, left_right[1]) for sub in left_right_terms[1] ])

def addAntonymAttribute(G: nx.DiGraph, attribute: str, left_right: (str, str), att_left_right: (Any, Any)) -> None:
  G.nodes[left_right[0]][attribute] = att_left_right[0]
  G.nodes[left_right[1]][attribute] = att_left_right[1]

def loadGraphFromFile(path:str):
  f = open(path)
  Gjson = json.load(f)
  return nx.node_link_graph(Gjson)