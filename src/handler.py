from business.candidate import CandidateBusiness
from business.job_post import JobPostBusiness
from business.matching import Matcher
from numpy import linalg as LA
import services.lang_processing as lp

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
import networkx as nx


client = MongoClient('mongodb+srv://user_imt:2020@s5resumesdb-ppukj.azure.mongodb.net/test')
print(client.list_database_names())
db = client['db']
print(db.list_collection_names())


# db_resumeSoveren = db['resumes_sovren']
# recent_resume_post = db_resumeSoveren.find_one({ '_id': ObjectId('5e60f5895a90883323e38bbc') })

# db_jobSoveren = db['jobs_sovren']
# recent_job_post = db_jobSoveren.find_one({ '_id': ObjectId('5e64cbef837ba015d90abc76') })


def db_job(db_name,id):
    db_Soveren = db[db_name]
    return db_Soveren.find_one({ '_id': ObjectId(id) })


def candidatePipeline(candidate_id):
    recent_resume_post = db_job('resumes_sovren',candidate_id)
    candidate_business = CandidateBusiness(recent_resume_post)
    candidate_jobdescription = candidate_business.upload(recent_resume_post)
    G3 = candidate_business.getCandidateSkillGraph(candidate_jobdescription)
    return G3

def jobPipeline(job_id):
    recent_job_post = db_job('jobs_sovren',job_id)
    job_post_business = JobPostBusiness(recent_job_post)
    job_post_jobdescription = job_post_business.upload(recent_job_post)
    print(job_post_jobdescription)
    G4 = job_post_business.getJobSkillGraph(job_post_jobdescription)
    return G4

# candidatePipeline()

def OnetoOnematching(candidate_id, job_id):
    candidate_graph = candidatePipeline(candidate_id)
    job_graph = jobPipeline(job_id)
    matching = Matcher(candidate_graph,job_graph)
    skills_match = matching.oneToOneMatch(candidate_graph,job_graph)
    model = lp.getGloveModel(300)
    culture_match = matching.getOneToOneCultureMatch(candidate_id, job_id, model, db['resumes_sovren'], db['jobs_sovren'])
    return skills_match, culture_match


def OnetoManymatching(candidate_id, job_id):
    candidateGraph = []
    job_graph = jobPipeline(job_id)
    for position in range(len(candidate_id)):
        candidateGraph.append(candidatePipeline(candidate_id[position]))
    matching = Matcher(candidateGraph,job_graph)
    return matching.onetoManyMatch(candidateGraph,job_graph)
    




def runOneToOne():
    skills_match, culture_match = OnetoOnematching('5e60f5895a90883323e38bbc','5e64cbef837ba015d90abc76')
    print('==========================')
    print(f'Skills Matching: {skills_match} %')
    print(f'Culture Matching: {culture_match} %')

runOneToOne()

#print('One to one matching of CV to the jobpost is ',OnetoManymatching(['5e60f5895a90883323e38bbc','5e60f5895a90883323e38bbc'],'5e64cbef837ba015d90abc76'))