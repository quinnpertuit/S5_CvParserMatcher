from handler import runOneToOne, runOneToMany, analysisAxes

analysis_types = [ 
  {
    'name': 'OneToOneMatching',
    'description': 'matches one CV to job posting from ids given',
    'function': runOneToOne,
    'inputs': ['candidate_id', 'job_id', 'explainable (True OR False)'],
    'input_validators': [str, str, bool],
    'input_functions': [ None, None, None ],
    'majority_rule_sorting': False
  },
  {
    'name': 'ManyToOneMatching',
    'description': 'matches several CVs to a job posting from ids given',
    'function': runOneToMany,
    'inputs': ['candidate_ids (write list of values comma separated)', 'job_id'],
    'input_validators': [list, str],
    'input_functions': [ lambda inp: [ i.strip(" '") for i in input(f'{inp} = ').split(',') ], None ],
    'majority_rule_sorting': True,
    'analysis_axes': analysisAxes
  }
]

def getAnalysisTypesString():
  analysisTypeToString = lambda at: f"{at['name']} ({at['description']})"
  return ''.join([f"{k+1}. - { analysisTypeToString(at) }\n" for k, at in enumerate(analysis_types)])

def askForInputs(i):
  print('Now, please type inputs:')
  if len(analysis_types[i]['inputs']) != len(analysis_types[i]['input_functions']): return []
  inputs = []
  for inp, f in zip(analysis_types[i]['inputs'], analysis_types[i]['input_functions']):
    if not f: inputs.append( input(f'{inp} = ') )
    else: inputs.append( f(inp) )
  return inputs

def askForWeights(i:int) -> dict:
  axes, errors = analysis_types[i]['analysis_axes'], False
  min_weight, max_weight = 0, 3
  weight_condition = lambda w: (0 <= w and w <= 3)
  s = '( ' + ''.join([ f"{i+1}: {axe['name']}, " if i != len(axes)-1 else f"{i+1}: {axe['name']}" for i, axe in enumerate(axes)]) + ' )'
  print(f"Finally, we need you to assign the weights you want to give for each of the study axes:"
    + f"\n## Axes ## { s }"
    + "\n\nAssign a value between [0, 3] which will explain how much you're interested in each axe of study,"
    + "\n => where { 0=Not interested, 1=little interested, 2=interested, 3=very interested }"
    + "\n* Separate the {len(axes)} values by a comma (ex: v1, v2, v3).")
  weights = input(f'values ({len(axes)} expected): ').split(',')
  weights = [ w.strip(" '") for w in weights ]
  if len(weights) != len(axes):
    print(f" -- Error -- Not enough weight inputs, expected {len(axes)}, received {len(weights)}. ")
    print(weights)
    return None
  for i, w in enumerate(weights): 
    try:
      weights[i] = int(w)
      if not weight_condition(weights[i]): 
        errors = True 
        print(f"-- Error: expecting value between {min_weight} and {max_weight}. But got {w}.")
    except: 
      errors = True
      print(f'-- Error: Incorrect type of input -- expecting integer, got { type(w) }')
  if errors: return None
  return { a['key_name']: w for a, w in zip(axes, weights) }

def validateInputs(inputs, validations):
  if len(inputs) != len(validations): return None
  errors = False
  for i, (v, c) in enumerate(zip(inputs, validations)):
    try:
      inputs[i] = c(v)
    except: 
      errors = True
      print(f'-- Error: Incorrect type of input -- expecting { c }, got { type(v) }')
  if errors: return None
  return inputs
    
def main():
  # Greeting
  print('\nHello!! :) \nPlease, tell us what type of analysis you would like to do:')
  # Type of Analysis
  print(getAnalysisTypesString())
  analysis_type_index = input('To choose an option, simply write the number: ')
  try:
    analysis_type_index = int(analysis_type_index) - 1
  except: 
    print('-- Error: Incorrect type of input')
  if analysis_type_index >= len(analysis_types): 
    print(f'-- Error: value not between 1 and {len(analysis_types)}')
    return
  # Get inputs for analysis
  print('\n--- INPUTS ---')
  inputs = askForInputs(analysis_type_index)
  inputs = validateInputs(inputs, analysis_types[analysis_type_index]['input_validators'])
  if not inputs: return

  # ask for weights
  weights = []
  if analysis_types[analysis_type_index]['majority_rule_sorting']: 
    print('\n--- WEIGHTS ---')
    weights = askForWeights(analysis_type_index)
    inputs.append(weights)
  
  print("\n--- Thanks!, now, we'll start calculating ----")
  # Run Analysis
  res = analysis_types[analysis_type_index]['function'](*inputs)
    

if __name__ == '__main__': 
  main()