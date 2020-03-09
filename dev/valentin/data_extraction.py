import numpy as np
from pymongo import MongoClient
from bson.objectid import ObjectId
import helpers as hp
from pprint import pprint as pp

MONGO_URL = 'mongodb+srv://user_imt:2020@s5resumesdb-ppukj.azure.mongodb.net/test'

def buildDescriptionsList(resumes: list) -> dict:
  desc = np.array([])
  for res in resumes:
    orgs = res['EmploymentHistory']['EmployerOrg']
    for org in orgs:
      roles = org['PositionHistory']
      for role in roles:
        desc = np.concatenate( (desc, [{
          'employer': org['EmployerOrgName'],
          'role': role['OrgName']['OrganizationName'],
          'description': role['Description'],
        }]))
  return desc


def getSummaries(resumes: list) -> str:
  return [ res['ExecutiveSummary'] for res in resumes ]


def getJobPostingFromFile(path:str) -> str:
  jp = open(path)
  return jp.read()

def loadResumes():
  client = MongoClient(MONGO_URL)
  db = client['db'] # db
  return db['resumes']

def getDescriptionsString(resumes):
  desc = buildDescriptionsList(resumes)
  description_list = hp.getValuesOfListOfDicts(desc, 'description')
  return hp.joinArrayOfStrings(description_list)

def getResumeString(db_resumes, n:int=1, o_id:ObjectId=None):
  resumes = db_resumes.find(limit=n) if not o_id else db_resumes.find_one({ '_id': o_id })
  resumes = list(resumes)
  summaries_string = " ".join(getSummaries(resumes))
  descriptions_string = getDescriptionsString(resumes)
  return summaries_string + " " + descriptions_string