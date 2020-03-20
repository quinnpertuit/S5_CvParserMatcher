from handler import runOneToOne, OnetoManymatching

analysis_types = [ 
  {
    'name': 'OneToOneMatching',
    'description': 'matches one CV to job posting from ids given',
    'function': runOneToOne,
    'inputs': ['candidate_id', 'job_id', 'explainable (True OR False)'],
    'input_validators': [str, str, bool]
  },
  {
    'name': 'ManyToOneMatching',
    'description': 'matches several CVs to a job posting from ids given',
    'function': OnetoManymatching,
    'inputs': ['candidate_id', 'job_id']
  }
]

def getAnalysisTypesString():
  analysisTypeToString = lambda at: f"{at['name']} ({at['description']})"
  return ''.join([f"{k+1}. - { analysisTypeToString(at) }\n" for k, at in enumerate(analysis_types)])

def askForInputs(i):
  print('\nNow, please type inputs:')
  return [ input(f'{inp} = ') for inp in analysis_types[i]['inputs'] ]

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
  print('\nHello!! :) \nPlease, tell us what type of analysis you would like to do:')
  print(getAnalysisTypesString())
  analysis_type_index = input('To choose an option, simply write the number: ')
  try:
    analysis_type_index = int(analysis_type_index) - 1
  except: 
    print('-- Error: Incorrect type of input')
  if analysis_type_index >= len(analysis_types) - 1: 
    print(f'-- Error: value not between 1 and {len(analysis_types)}')
    return
  inputs = askForInputs(analysis_type_index)
  inputs = validateInputs(inputs, analysis_types[analysis_type_index]['input_validators'])
  if not inputs: return
  #printvals(*inputs)
  analysis_types[analysis_type_index]['function'](*inputs)


if __name__ == '__main__': 
  main()