import networkx as nx
import classifier.classifier as classifier
from fuzzywuzzy import process

from services.data_extraction.job_post.jobpost import JobDataExtraction

class JobDataProcessing:
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

    def getNormalizedDegreeEducation(self, dict_job_education):
        degree_dict = {'master' : 5, 'msc': 5, 'Bac +5' : 5, 'bachelor':4, 'bac +4' : 4, 'B.Tech' : 4, 'B.E' :4}
        highest = process.extractOne(dict_job_education['DegreeName']['DegreeName'],degree_dict.keys())
        return degree_dict[highest[0]]

    def getJobSkills(self, jsonobject):
        skillDict ={}
        requiredSkill = []
        desiredSkill = []
        #extract information technology Skill taxanomy at the index 0
        Job_data_extraction = JobDataExtraction(jsonobject)

        InformationTaxanomy = jsonobject['SovrenData']['SkillsTaxonomyOutput'][0]['Taxonomy'][0]
        requiredSkill = Job_data_extraction.getJobPostSkill(InformationTaxanomy, Required= True)
        desiredSkill = Job_data_extraction.getJobPostSkill(InformationTaxanomy, Required= False)
        #extract engineering Skill taxanomy at the index 1
        EngineeringTaxanomy = jsonobject['SovrenData']['SkillsTaxonomyOutput'][0]['Taxonomy'][1]
        requiredSkill.extend(Job_data_extraction.getJobPostSkill(EngineeringTaxanomy, Required= True))
        desiredSkill.extend(Job_data_extraction.getJobPostSkill(EngineeringTaxanomy, Required= False))

        skillDict['requiredSkill']= requiredSkill
        skillDict['desiredSkill']= desiredSkill
        return skillDict
