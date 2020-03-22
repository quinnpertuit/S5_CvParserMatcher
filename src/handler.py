from business.candidate import CandidateBusiness
from business.job_post import JobPostBusiness
from business.matching import Matcher
from numpy import linalg as LA
import services.lang_processing as lp

##################################################


import pymongo
from pymongo import MongoClient
import ssl
from bson.objectid import ObjectId
import numpy as np
import networkx as nx


client = MongoClient('mongodb+srv://user_imt:2020@s5resumesdb-ppukj.azure.mongodb.net/test',ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
print(client.list_database_names())
db = client['db']
print(db.list_collection_names())


# db_resumeSoveren = db['resumes_sovren']
# recent_resume_post = db_resumeSoveren.find_one({ '_id': ObjectId('5e60f5895a90883323e38bbc') })

# db_jobSoveren = db['jobs_sovren']
# recent_job_post = db_jobSoveren.find_one({ '_id': ObjectId('5e64cbef837ba015d90abc78') })


def db_job(db_name,id):
    db_Soveren = db[db_name]
    return db_Soveren.find_one({ '_id': ObjectId(id) })


def candidatePipeline(candidate_id):
    recent_resume_post = db_job('resumes_sovren',candidate_id)
    candidate_business = CandidateBusiness(recent_resume_post)
    candidate_jobdescription,education_dict = candidate_business.download(recent_resume_post)
    candidate_job_dict,candidate_domain_skill_dict = candidate_business.getCandidateSkillDict(candidate_jobdescription)
    
    # to create over all skill graph
    G3 = candidate_business.getCandidateSkillGraph(candidate_job_dict)

    # to create data science domain Graph
    G_candidate_domain = candidate_business.getCandidateSkillGraph(candidate_domain_skill_dict)
    degree_level = candidate_business.getCandidateEducationDegree(education_dict)
    candidate_unique_skill = candidate_business.getCandidateUnionSkill(candidate_job_dict)
    return G3, G_candidate_domain,degree_level,candidate_unique_skill

def jobPipeline(job_id):
    recent_job_post = db_job('jobs_sovren',job_id)
    job_post_business = JobPostBusiness(recent_job_post)
    job_post_jobdescription,job_education_dict = job_post_business.download(recent_job_post)

    jobpost_job_dict,jobpost_domain_skill_dict = job_post_business.getJobSkillDict(job_post_jobdescription)

    # to create over all skill graph
    G4 = job_post_business.getJobSkillGraph(jobpost_job_dict)

    # to create data science domain Graph
    G_job_domain = job_post_business.getJobSkillGraph(jobpost_domain_skill_dict)
    degree_level = job_post_business.getJobEducationDegree(job_education_dict)
    job_required_skill = job_post_business.getJobRequiredSkill(recent_job_post)
    return G4 ,G_job_domain,degree_level,job_required_skill

def OnetoOnematching(candidate_id, job_id):
    culture_match = None
    candidate_graph, candidate_domian_graph,candidate_degree,candidate_unique_skill = candidatePipeline(candidate_id)
    job_graph, job_domian_graph,job_degree,job_required_skill = jobPipeline(job_id)
    matching = Matcher(candidate_graph,job_graph)
    skills_match = matching.oneToOneAllSkillMatch(candidate_graph,job_graph)
    required_skill_match = matching.getRequiredSkillMatch(job_required_skill,candidate_unique_skill)
    domain_skills_match = matching.oneToOneDomainSkillMatch(candidate_domian_graph,job_domian_graph)
    model = lp.getGloveModel(300)
    culture_match = matching.getOneToOneCultureMatch(candidate_id, job_id, model, db['resumes_sovren'], db['jobs_sovren'])
    string_education_match, _, _ = matching.educationDegreeMatch(candidate_degree,job_degree)
    
    return skills_match, domain_skills_match,culture_match, required_skill_match, string_education_match, ''



def OnetoManymatching(candidate_id, job_id):
    candidate_graph_list = []
    candidate_domain_graph_list= []
    required_skill = []
    job_graph, job_domian_graph,job_degree,job_required_skill = jobPipeline(job_id)
    matching = Matcher()
    for position in range(len(candidate_id)):
        candidate_graph, candidate_domian_graph,candidate_degree,candidate_unique_skill = candidatePipeline(candidate_id[position])
        candidate_graph_list.append(candidate_graph)
        candidate_domain_graph_list.append(candidate_domian_graph)
        matching.educationDegreeMatch(candidate_degree,job_degree)
        required_skill.append(matching.getRequiredSkillMatch(job_required_skill,candidate_unique_skill))
    Overall_skill_match = matching.onetoManyAllSkillMatch(candidate_graph_list,job_graph)
    Overall_domain_match = matching.onetoManyDomainSkillMatch(candidate_domain_graph_list,job_graph)
    return Overall_skill_match ,Overall_domain_match, required_skill

# print('One to one matching of CV to the jobpost is ',OnetoOnematching('5e60f5895a90883323e38bbc','5e64cbef837ba015d90abc78'))

# print('One to one matching of CV to the jobpost is ',OnetoManymatching(['5e60f5895a90883323e38bbc','5e60f5895a90883323e38bbc'],'5e64cbef837ba015d90abc78'))


################################################################################################


def runOneToOne(candidate_id, job_id, explainable=False):
    skills_match,domain_skills_match, culture_match, required_skill_match, string_education_match, explained_culture_match = OnetoOnematching(candidate_id, job_id)
    print('\n==========================')
    print('\n======== RESULT ==========')
    if explainable: print(explained_culture_match)
    print(f'Overall Culture Matching: {culture_match} %')
    print(string_education_match)
    print(f'Domain_Skills Matching: {domain_skills_match} %')
    print(f'OverAllSkills Matching: {skills_match} %')
    print(f'Required Skill Matching: {required_skill_match} %')

runOneToOne('5e60f5895a90883323e38bbc','5e64cbef837ba015d90abc78', True)

# print('One to one matching of CV to the jobpost is ',OnetoManymatching(['5e60f5895a90883323e38bbc','5e60f5895a90883323e38bbc'],'5e64cbef837ba015d90abc76'))