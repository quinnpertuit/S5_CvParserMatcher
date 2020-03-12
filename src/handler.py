from business.candidate import CandidateBusiness
from business.job_post import JobPostBusiness
from business.matching import Matcher
from numpy import linalg as LA

########################################################
#test code directly from handler

from services.data_extraction.job_post.jobpost import JobDataExtraction
##################################################


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

db_jobSoveren = db['jobs_sovren']
recent_job_post = db_jobSoveren.find_one({ '_id': ObjectId('5e64cbef837ba015d90abc78') })


def db_job(db_name,id):
    db_Soveren = db[db_name]
    return db_Soveren.find_one({ '_id': ObjectId(id) })


def candidatePipeline(candidate_id):
    recent_resume_post = db_job('resumes_sovren',candidate_id)
    candidate_business = CandidateBusiness(recent_resume_post)
    candidate_jobdescription,education_dict = candidate_business.upload(recent_resume_post)
    G3 = candidate_business.getCandidateSkillGraph(candidate_jobdescription)
    degree_level = candidate_business.getCandidateEducationDegree(education_dict)
    return G3, degree_level

def jobPipeline(job_id):
    recent_job_post = db_job('jobs_sovren',job_id)
    job_post_business = JobPostBusiness(recent_job_post)
    job_post_jobdescription,job_education_dict = job_post_business.upload(recent_job_post)
    G4 = job_post_business.getJobSkillGraph(job_post_jobdescription)
    degree_level = job_post_business.getJobEducationDegree(job_education_dict)
    return G4 ,degree_level

# candidatePipeline()
def educationDegreeMatch(jobDegree, candidateDegree):
    if (jobDegree == candidateDegree):
        print('The candidate degree matches to the job profile')
    elif(jobDegree > candidateDegree):
        print('The candidate degree doesn not matches to the job profile')
    elif(jobDegree < candidateDegree):
        print('The candidate degree overqualified matches to the job profile')


def OnetoOnematching(candidate_id, job_id):
    candidate_graph, candidate_degree = candidatePipeline(candidate_id)
    job_graph, job_degree = jobPipeline(job_id)
    matching = Matcher(candidate_graph,job_graph)
    educationDegreeMatch(candidate_degree,job_degree)
    return matching.oneToOneMatch(candidate_graph,job_graph)


def OnetoManymatching(candidate_id, job_id):
    candidateGraph = []
    job_graph = jobPipeline(job_id)
    for position in range(len(candidate_id)):
        candidateGraph.append(candidatePipeline(candidate_id[position]))
    matching = Matcher(candidateGraph,job_graph)
    return matching.onetoManyMatch(candidateGraph,job_graph)
print('One to one matching of CV to the jobpost is ',OnetoOnematching('5e60f5895a90883323e38bbc','5e64cbef837ba015d90abc78'))

# print('One to one matching of CV to the jobpost is ',OnetoManymatching(['5e60f5895a90883323e38bbc','5e60f5895a90883323e38bbc'],'5e64cbef837ba015d90abc76'))


################################################################################################
#education System




# jobPipeline('5e64cbef837ba015d90abc78')
