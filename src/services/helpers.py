import numpy as np
from functools import reduce
import re
from math import sqrt

def getItemsContainedInListAndNot(candidates: list, list_to_compare: list) -> (list, list):
  found = []; not_found = []
  for item in candidates:
    if item in list_to_compare: found.append(item)
    else: not_found.append(item)
  return found, not_found

def getItemsContainedInList(candidates: list, list_to_compare: list):
  return [ item for item in candidates if item in list_to_compare ]

def getValuesOfListOfDicts(l: list, key: str) -> list:
  return np.array([ e[key] for e in l ])

def joinArrayOfStrings(l: list) -> str:
  return reduce(lambda s1, s2: f'{s1} {s2}', l)

def showAroundStrings(left:int, s:str, right:int, phrase:str, display:bool = True):
  for e in re.finditer(s, phrase):
    start = e.start()
    end = e.end()
    if display: print(f'{s}\t « { phrase[(start - left):(end + right)] } »')

def calculateMeanOfListOfTuples(l: list, key, starting_value=0):
  return reduce(lambda acc, t: acc + t[key], l, starting_value) / len(l)

def euclidean_distance(x,y):
  return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))