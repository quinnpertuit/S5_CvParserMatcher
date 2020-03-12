import gmatch4py as gm
import os
from numpy import linalg as LA
from business.candidate import CandidateBusiness
from business.job_post import JobPostBusiness
import services.graph_treat as gt
import services.helpers as hp

class Matcher:

    def __init__(self,G_candidate,G_jobPost):
        self.G_candidate = G_candidate
        self.G_jobPost = G_jobPost
        self.culture_graph_path = '../graphs/culture_graph.json' 
    
    def oneToOneMatch(self, G_candidate, G_jobPost):
        ged=gm.GraphEditDistance(1,1,1,1) # all edit costs are equal to 1
        result=ged.compare([G_candidate,G_jobPost],None) 
        #description how much score is and why it got mactched
        return LA.norm(ged.similarity(result))

    def onetoManyMatch(self, G_candidate, G_jobPost):
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

