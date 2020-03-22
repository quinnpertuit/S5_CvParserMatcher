import pandas as pd
from typing import List, Any, Tuple
import numpy as np
from pprint import pprint as pp

class FilterSortBusiness:
  def __init__(self):
    return

  def MRSorting(self, values:dict, weights:dict, min_max:dict) -> pd.DataFrame:
    """
    Adaptation of the Multi Criteria Majority Rule Sorting algorithm
    
    Patameters
    ---------
    values: the values of each axe concerned for sorting for all the desired CVs
    weights: the weights assigned from the user for each of the axis
    min_max: dict of axes containing { [axe]: { 'min': _, 'max': _ ...} ... } values
    """
    values, total_axes, sum_weights, majority_rule_values = pd.DataFrame(values), len(weights), sum(weights.values()), []
    if total_axes != len(min_max) or total_axes != values.shape[1]: 
      print(f" --- Error: not expected sizes (total_axes, min_max, values) ({total_axes}, {len(min_max)}, {values.shape[1]})")
      return None
    norm_weights = { k: w / sum_weights for k, w in weights.items() }
    for _, row in values.iterrows():
      mjv = 0
      for axe_type, v in row.items():
        axe_min, axe_max, w = min_max[axe_type]['min'], min_max[axe_type]['max'], norm_weights[axe_type]
        if axe_min == None or axe_max == None: axe_min, axe_max = 0, v # handle not known ranges
        normalized_v = (v - axe_min) / (axe_max - axe_min) if axe_max != 0 and axe_max != axe_min else 0
        mjv += normalized_v * w
      majority_rule_values.append(mjv)
    values['MRValues'] = majority_rule_values
    return values.sort_values(by='MRValues', ascending=False)

  def filterCVs(self, values:dict, required:dict) -> (list, list, pd.DataFrame):
    """
    Filter CVs from criteria given
    
    Parameters
    ---------
    values: the values of each axe concerned for filtering for all the desired CVs
    required: dict of axes containing { [axe]: { 'required': _, ...} ... } values
    """
    values, total_axes = pd.DataFrame(values), values.shape[1]
    if total_axes != len(required): 
      print(f" --- Error: not expected sizes (total_axes, required, values) ({total_axes}, {len(required)}, {values.shape[1]})")
      return None
    ids_to_maintain, ids_to_drop = [], []
    for iid, row in values.iterrows():
      for axe_type, v in row.items():
        if v < required[axe_type]: ids_to_drop.append(iid)
        else: ids_to_maintain.append(iid)
    return ids_to_maintain, ids_to_drop, values.loc[ ids_to_drop ]


