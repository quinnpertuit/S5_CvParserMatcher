######################This section deals with the skills from the job description#######################
import classifier.classifier as classifier
import networkx as nx


def collectJobDescriptionSkill(jsonobject):
    skillDict ={}
    requiredSkill = []
    desiredSkill = []
    #extract information technology Skill taxanomy at the index 0
    InformationTaxanomy = jsonobject['SovrenData']['SkillsTaxonomyOutput'][0]['Taxonomy'][0]
    requiredSkill = getJobSkill(InformationTaxanomy, Required= True)
    desiredSkill = getJobSkill(InformationTaxanomy, Required= False)
    #extract engineering Skill taxanomy at the index 1
    EngineeringTaxanomy = jsonobject['SovrenData']['SkillsTaxonomyOutput'][0]['Taxonomy'][1]
    requiredSkill.extend(getJobSkill(EngineeringTaxanomy, Required= True))
    desiredSkill.extend(getJobSkill(EngineeringTaxanomy, Required= False))

    skillDict['requiredSkill']= requiredSkill
    skillDict['desiredSkill']= desiredSkill
    return skillDict


def getJobSkill(jsonTaxanomy, Required = False):
    skill = []
    for i in range(0,len(jsonTaxanomy)):
        for j in range(0,len(jsonTaxanomy['Subtaxonomy'][i]['Skill'])):
            dictSkill = jsonTaxanomy['Subtaxonomy'][i]['Skill'][j]
            if dictSkill["@existsInText"]== True and dictSkill["@required"]== Required:
                skill.append(dictSkill['@name'])
            if "ChildSkill" in  dictSkill.keys() and dictSkill["ChildSkill"][0]["@existsInText"]== True and dictSkill["ChildSkill"][0]["@required"]== Required:
                skill.append(dictSkill["ChildSkill"][0]['@name'])
    return skill

######################This section deals with the skills from the Candidate resume#######################

# to extract all the workexperience description in the CV
def CandidateSkillDescription(candidateDescription):
    JobDescription = ''
    count = len(candidateDescription['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg'])
    for i in range(0,count):
        JobDescription += candidateDescription['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg'][i]['PositionHistory'][0]['Description']
    return JobDescription


# to extract all the workexperience description in the CV

def getJobDescriptionText(jobPost):
    return jobPost['SovrenData']['SourceText']

# to generate skill graph from the workexperience description in the CV

def getSkillOntoloies(workExpDescription):
    generateSkillLink = {}
    prepareText = {'keywords':"data mining, computer science"}
    prepareText['abstract']=workExpDescription
    result = classifier.run_cso_classifier(prepareText, modules = "both", enhancement = "first", explanation = True)
    generateSkill['union'] = result['union']
    generateSkill['explanation'] = result['explanation']
    return generateSkillLink


def addEdge(graph,u,v): 
    graph[u].append(v) 
  
# definition of function 
def generate_edges(graph): 
    edges = [] 
    # for each node in graph 
    for node in graph: 
        # for each neighbour node of a single node 
        for neighbour in graph[node]: 
            # if edge exists then append 
            edges.append((node, neighbour)) 
    return edges

def generateSkillGraph(generateSkillLink):
    G2=nx.Graph()
    G2.add_edges_from(generate_edges(generateSkillLink['explanation']))
    return G2



############################ This section deals with the education ##############################
########to do

def EducationRequirement(candidate_education, job_description_education):
    normalize_candidate_education = NormalizeEducation(candidate_education)
    normalize_job_education = NormalizeEducation(job_description_education)
    if (normalize_candidate_education == normalize_job_education):
        return "The education level matches between both"
    elif (normalize_candidate_education > normalize_job_education):
        return "candidate is over qualified "
    elif (normalize_candidate_education < normalize_job_education):
        return "candidate is not qualified for the job "



def NormalizeEducation(education_name):
    bachelorsList = ["bachelors", "Bac+4", "bachelor"]
    masterList = ["master", "masters", "Bac+5", "Bac +5"]

    if education_name in bachelorsList:
        return 4
    elif education_name in masterList:
        return 5
    