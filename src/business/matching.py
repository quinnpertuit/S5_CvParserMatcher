import gmatch4py as gm
from numpy import linalg as LA

class Matcher:

    def __init__(self,G_candidate,G_jobPost):
        self.G_candidate = G_candidate
        self.G_jobPost = G_jobPost
    
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

