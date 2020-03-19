import gmatch4py as gm
import os
from numpy import linalg as LA
from business.candidate import CandidateBusiness
from business.job_post import JobPostBusiness
import services.graph_treat as gt
import services.helpers as hp

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
        cv_vec = [ t[0] for k, t in dict_antonyms.items() ]
        jp_vec = [ t[1] for k, t in dict_antonyms.items() ]
        return 1 - hp.euclidean_distance(cv_vec, jp_vec) #1 better, 0 worst


    def getRequiredSkillMatch(self,required_job_skill, candidate_skill):
        j=0
        for i in range(0,len(required_job_skill)):
            if required_job_skill[i].lower() in candidate_skill:
                j = j+1
        return j/len(required_job_skill)

    def educationDegreeMatch(self,jobDegree, candidateDegree):
        if (jobDegree == candidateDegree):
            print('The candidate degree matches to the job profile')
        elif(jobDegree > candidateDegree):
            print('The candidate degree doesn not matches to the job profile')
        elif(jobDegree < candidateDegree):
            print('The candidate degree overqualified matches to the job profile')

