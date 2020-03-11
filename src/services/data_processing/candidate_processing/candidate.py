import networkx as nx
import classifier.classifier as classifier

class CandidateDataProcessing:
    def __init__(self):
        classifier.setup()
        return

    def getSkillOntoloies(self,workExpDescription):
        generateSkillLink = {}
        prepareText = {'keywords':"data mining, computer science"}
        prepareText['abstract']=workExpDescription
        result = classifier.run_cso_classifier(prepareText, modules = "both", enhancement = "first", explanation = True)
        generateSkill['union'] = result['union']
        generateSkill['explanation'] = result['explanation']
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

    def generateSkillGraph(self,generateSkillLink):
        G2=nx.Graph()
        G2.add_edges_from(generate_edges(generateSkillLink['explanation']))
        return G2
