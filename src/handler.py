from business.candidate import CandidateBusiness

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np



client = MongoClient('mongodb+srv://user_imt:2020@s5resumesdb-ppukj.azure.mongodb.net/test')
print(client.list_database_names())
db = client['db']
print(db.list_collection_names())
db_jobSoveren = db['resumes_sovren']
recent_jobPost = db_jobSoveren.find_one({ '_id': ObjectId('5e60f5895a90883323e38bbc') })

def CandidatePipeline():
    candidate_business = CandidateBusiness(recent_jobPost)
    candidate_jobdescription = candidate_business.upload(recent_jobPost)
    print(candidate_business)

CandidatePipeline()