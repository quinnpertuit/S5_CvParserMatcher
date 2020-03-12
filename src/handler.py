from business.candidate import CandidateBusiness
from business.job_post import JobPostBusiness
from business.matching import Matcher
from numpy import linalg as LA

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
import networkx as nx


client = MongoClient('mongodb+srv://user_imt:2020@s5resumesdb-ppukj.azure.mongodb.net/test')
print(client.list_database_names())
db = client['db']
print(db.list_collection_names())
db_resumeSoveren = db['resumes_sovren']
recent_resume_post = db_resumeSoveren.find_one({ '_id': ObjectId('5e60f5895a90883323e38bbc') })

db_jobSoveren = db['jobs_sovren']
recent_job_post = db_jobSoveren.find_one({ '_id': ObjectId('5e64cbef837ba015d90abc76') })


def candidatePipeline():
    candidate_business = CandidateBusiness(recent_resume_post)
    candidate_jobdescription = candidate_business.upload(recent_resume_post)
    G3 = candidate_business.getCandidateSkillGraph(candidate_jobdescription)
    return G3

def jobPipeline():
    job_post_business = JobPostBusiness(recent_job_post)
    job_post_jobdescription = job_post_business.upload(recent_job_post)
    print(job_post_jobdescription)
    G4 = job_post_business.getJobSkillGraph(job_post_jobdescription)
    return G4

# candidatePipeline()

def matching():
    candidate_graph = candidatePipeline()
    job_graph = jobPipeline()
    matching = Matcher(candidate_graph,job_graph)
    return matching.oneToOneMatch(candidate_graph,job_graph)

print('The match score of CV to the jobpost is ',LA.norm(matching()))