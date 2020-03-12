import gmatch4py as gm

class Matcher:

    def __init__(self,G_candidate,G_jobPost):
        self.G_candidate = G_candidate
        self.G_jobPost = G_jobPost
        return
    
    def oneToOneMatch(self, G_candidate, G_jobPost):
        ged=gm.GraphEditDistance(1,1,1,1) # all edit costs are equal to 1
        result=ged.compare([G_candidate,G_jobPost],None) 
        #description how much score is and why it got mactched
        return ged.similarity(result)

    def onetoManyMatch(self):
        # matchCVToJP
        return