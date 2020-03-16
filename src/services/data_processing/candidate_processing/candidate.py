import networkx as nx
import classifier.classifier as classifier
from fuzzywuzzy import process

class CandidateDataProcessing:
    def __init__(self,workExpDescription):
        self.workExpDescription =workExpDescription
        classifier.setup()
        return

    def getSkillOntoloies(self,workExpDescription):
        generateSkillLink = {}
        prepareText = {'keywords':"data mining, computer science"}
        prepareText['abstract']=workExpDescription
        result = classifier.run_cso_classifier(prepareText, modules = "both", enhancement = "first", explanation = True)
        generateSkillLink['union'] = result['union']
        generateSkillLink['explanation'] = result['explanation']
        return generateSkillLink

    # definition of function 
    def generate_edges(self,graph): 
        edges = [] 
        # for each node in graph 
        for node in graph: 
            # for each neighbour node of a single node 
            for neighbour in graph[node]: 
                # if edge exists then append 
                edges.append((node, neighbour)) 
        return edges

    def generateSkillGraph(self,edges):
        G2=nx.Graph()
        G2.add_edges_from(edges)
        return G2

    def getNormalizedSchoolEducation(self):
        school_dict = {'grand ecole' : 5, 'university': 4}
        return

    def getNormalizedDegreeEducation(self, dict_candidate_education):
        degree_dict = {'master' : 5, 'msc': 5, 'Bac +5' : 5, 'bachelor':4, 'bac +4' : 4, 'B.Tech' : 4, 'B.E' :4}
        highest = process.extractOne(dict_candidate_education['DegreeName'],degree_dict.keys())
        return degree_dict[highest[0]]

    
