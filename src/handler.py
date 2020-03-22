from business.candidate import CandidateBusiness
from business.job_post import JobPostBusiness
from business.matching import Matcher
from business.filter_sort import FilterSortBusiness
from numpy import linalg as LA
import services.lang_processing as lp

##################################################


import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
import networkx as nx
from pprint import pprint as pp
import pandas as pd

client = MongoClient('mongodb+srv://user_imt:2020@s5resumesdb-ppukj.azure.mongodb.net/test')
#print(client.list_database_names())
db = client['db']
#print(db.list_collection_names())

# db_resumeSoveren = db['resumes_sovren']
# recent_resume_post = db_resumeSoveren.find_one({ '_id': ObjectId('5e60f5895a90883323e38bbc') })

# db_jobSoveren = db['jobs_sovren']
# recent_job_post = db_jobSoveren.find_one({ '_id': ObjectId('5e64cbef837ba015d90abc78') })

word2VecDimensions = 50 # there are also files of 50, 100, 200, 300 dimensions (remainder: they should be inserted in the models folder)
analysisAxes = [
    {
        'name': 'Skills Match',
        'key_name': 'skills_match',
        'min': None,
        'max': None,
    },
    {
        'name': 'Domain Skills Match',
        'key_name': 'domain_skills_match',
        'min': None,
        'max': None,
    },
    {
        'name': 'Culture Match',
        'key_name': 'culture_match',
        'min': -1,
        'max': 1,
    },
    {
        'name': 'Required Skills Match',
        'key_name': 'required_skill_match',
        'min': 0,
        'max': 1,
    }
]

filterAxes = [
    {
        'name': 'Education Match',
        'key_name': 'education_match',
        'min': 0,
        'max': 1,
        'required': 1,
    }
]

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
    culture_match, explained_culture_match = None, ''    
    candidate_graph, candidate_domian_graph,candidate_degree,candidate_unique_skill = candidatePipeline(candidate_id)
    job_graph, job_domian_graph,job_degree,job_required_skill = jobPipeline(job_id)
    matching = Matcher(candidate_graph,job_graph)
    skills_match = matching.oneToOneAllSkillMatch(candidate_graph,job_graph)
    required_skill_match = matching.getRequiredSkillMatch(job_required_skill,candidate_unique_skill)
    domain_skills_match = matching.oneToOneDomainSkillMatch(candidate_domian_graph,job_domian_graph)
    model = lp.getGloveModel(word2VecDimensions)
    explained_culture_match, culture_match = matching.getOneToOneCultureMatch(candidate_id, job_id, model, db['resumes_sovren'], db['jobs_sovren'])
    string_education_match, _, _ = matching.educationDegreeMatch(candidate_degree,job_degree)
    return {
        'skills_match': skills_match,
        'domain_skills_match': domain_skills_match,
        'culture_match': culture_match,
        'required_skill_match': required_skill_match, 
        'string_education_match': string_education_match, 
        'explained_culture_match': explained_culture_match,
        }



def OnetoManymatching(candidate_id, job_id):
    candidate_domain_graph_list, required_skill, candidate_graph_list, culture_match_list, education_match_list = [], [], [], [], []
    job_graph, job_domian_graph,job_degree,job_required_skill = jobPipeline(job_id)
    matching = Matcher()
    model = lp.getGloveModel(word2VecDimensions)
    for position in range(len(candidate_id)):
        candidate_graph, candidate_domian_graph,candidate_degree,candidate_unique_skill = candidatePipeline(candidate_id[position])
        candidate_graph_list.append(candidate_graph)
        candidate_domain_graph_list.append(candidate_domian_graph)
        _, jobDegree, candidateDegree = matching.educationDegreeMatch(candidate_degree,job_degree)
        education_match_list.append(candidateDegree / jobDegree)
        _, culture_match = matching.getOneToOneCultureMatch(candidate_id[position], job_id, model, db['resumes_sovren'], db['jobs_sovren'])
        culture_match_list.append(culture_match)
        required_skill.append(matching.getRequiredSkillMatch(job_required_skill,candidate_unique_skill))
    overall_skill_match = matching.onetoManyAllSkillMatch(candidate_graph_list,job_graph)
    overall_domain_match = matching.onetoManyDomainSkillMatch(candidate_domain_graph_list,job_graph)
    return {
        'domain_skills_match': overall_domain_match,
        'skills_match': overall_skill_match,
        'required_skill_match': required_skill,
        'culture_match': culture_match_list,
        'education_match': education_match_list,
    }

# print('One to one matching of CV to the jobpost is ',OnetoOnematching('5e60f5895a90883323e38bbc','5e64cbef837ba015d90abc78'))

# print('One to one matching of CV to the jobpost is ',OnetoManymatching(['5e60f5895a90883323e38bbc','5e60f5895a90883323e38bbc'],'5e64cbef837ba015d90abc78'))

#r = OnetoManymatching(['5e60f5895a90883323e38bbb','5e60f5895a90883323e38bbc'],'5e64cbef837ba015d90abc78')
#pp(r)
################################################################################################


def runOneToOne(candidate_id, job_id, explainable=False):
    otom_res = OnetoOnematching(candidate_id, job_id)
    #skills_match, culture_match, required_skill_match, string_education_match, explained_culture_match = 
    print('\n==========================')
    print('\n======== RESULT ==========')
    if explainable: print(otom_res['explained_culture_match'])
    print(f"Overall Culture Matching: {otom_res['culture_match']} %")
    print(otom_res['string_education_match'])
    print(f"Domain_Skills Matching: {otom_res['domain_skills_match']} %")
    print(f"OverAllSkills Matching: {otom_res['skills_match']} %")
    print(f"Required Skill Matching: {otom_res['required_skill_match']} %")
    return [otom_res]

def runOneToMany(candidate_ids, job_id, weights, filterAxes=filterAxes, analysisAxes=analysisAxes):
    matches = OnetoManymatching(candidate_ids, job_id)
    matches = pd.DataFrame(matches, index=candidate_ids)
    fsb = FilterSortBusiness()
    filter_key_names, analysis_key_names = [ a['key_name'] for a in filterAxes ], [ a['key_name'] for a in analysisAxes ]
    filter_matches, analysis_matches = matches[ filter_key_names ], matches[ analysis_key_names ]
    ids_maintain, ids_drop, filtered_matches = fsb.filterCVs(filter_matches, { axe['key_name']: axe['required'] for axe in filterAxes if axe['key_name'] in filter_matches })
    analysis_matches = analysis_matches.loc[ ids_maintain ]
    sorted_matches = fsb.MRSorting(analysis_matches, weights, { axe['key_name']: {'min': axe['min'],'max': axe['max']} for axe in analysisAxes if axe['key_name'] in analysis_matches })
    print('\n==========================')
    print('\n======== RESULT ==========')
    print(f"The next CVs were ignored completely due to { ', '.join([ a['name'] for a in filterAxes ]) } considerations: \n{ ids_drop }")
    print(f"The classification of the CVs is the next one: \n")
    print(sorted_matches['MRValues'])
    return filtered_matches, sorted_matches


# runOneToOne('5e60f5895a90883323e38bbc','5e64cbef837ba015d90abc78', True)

# print('One to one matching of CV to the jobpost is ',OnetoManymatching(['5e60f5895a90883323e38bbc','5e60f5895a90883323e38bbc'],'5e64cbef837ba015d90abc76'))