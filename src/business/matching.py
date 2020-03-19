import gmatch4py as gm
import os
from numpy import linalg as LA
from business.candidate import CandidateBusiness
from business.job_post import JobPostBusiness
import services.graph_treat as gt
import services.helpers as hp
from pprint import pprint as pp

class Matcher:

    def __init__(self,G_candidate = None,G_jobPost =None):
        self.G_candidate = G_candidate
        self.G_jobPost = G_jobPost
        self.culture_graph_path = '../graphs/culture_graph.json' 
    
    def oneToOneAllSkillMatch(self, G_candidate, G_jobPost):
        ged=gm.GraphEditDistance(1,1,1,1) # all edit costs are equal to 1
        result=ged.compare([G_candidate,G_jobPost],None) 
        #description how much score is and why it got mactched
        return LA.norm(ged.similarity(result))

    def onetoManyAllSkillMatch(self, G_candidate, G_jobPost):
        matching_Score=[]
        for graph in G_candidate:
            ged=gm.GraphEditDistance(1,1,1,1) # all edit costs are equal to 1
            result=ged.compare([graph,G_jobPost],None)
            matching_Score.append(LA.norm(ged.similarity(result)))
        # matchCVToJP
        return matching_Score

    def oneToOneDomainSkillMatch(self, G_candidate_domain, G_jobPost_domain):
        ged=gm.GraphEditDistance(1,1,1,1) # all edit costs are equal to 1
        result=ged.compare([G_candidate_domain,G_jobPost_domain],None) 
        #description how much score is and why it got mactched
        return LA.norm(ged.similarity(result))

    def onetoManyDomainSkillMatch(self, G_candidate, G_jobPost):
        matching_Score=[]
        for graph in G_candidate:
            ged=gm.GraphEditDistance(1,1,1,1) # all edit costs are equal to 1
            result=ged.compare([graph,G_jobPost],None)
            matching_Score.append(LA.norm(ged.similarity(result)))
        # matchCVToJP
        return matching_Score


    def getOneToOneCultureMatch(self, candidate_id, job_post_id, model, cv_coll, job_coll):
        bs_c, bs_jp = CandidateBusiness(None), JobPostBusiness(None)
        built_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.culture_graph_path))
        G_cand = bs_c.getCandidateCultureEvaluatedGraph(candidate_id, built_path, model, cv_coll)
        G_jobp = bs_jp.getJobPostCultureEvaluatedGraph(job_post_id, built_path, model, job_coll)
        dict_antonyms = gt.getTwoGraphsAttributeInfo(G_cand, G_jobp, 6, 'similarity')
        explainable_string = "\nCulture match has been done with Word2Vec approach, so values mean how related the cultural terms are to CV ones.\n* For definitions, please, look up on article\n(<CV_to_Culture_similarity>, <Job_Posting_to_Culture_similarity>) <- <Cultural_aspect_evaluated>\n"
        explainable_string += ''.join([ f"({round(t[0]*100, 2)}, {round(t[1]*100, 2)}) <- { ' '.join(k.split('_')) }\n" for k, t in dict_antonyms.items() ])
        cv_vec, jp_vec = [ t[0] for k, t in dict_antonyms.items() ], [ t[1] for k, t in dict_antonyms.items() ]
        return explainable_string, 1 - hp.euclideanDistance(cv_vec, jp_vec) #1 better, 0 worst


    def getRequiredSkillMatch(self,required_job_skill, candidate_skill):
        j=0
        for i in range(0,len(required_job_skill)):
            if required_job_skill[i].lower() in candidate_skill:
                j = j+1
        return j/len(required_job_skill)

    def educationDegreeMatch(self,jobDegree, candidateDegree):
        s = ''
        if (jobDegree == candidateDegree):
            s = 'The candidate degree matches to the job profile'
        elif(jobDegree > candidateDegree):
            s = 'The candidate degree does not matches to the job profile'
        elif(jobDegree < candidateDegree):
            s = 'The candidate degree overqualified matches to the job profile'
        return s, jobDegree, candidateDegree

