import datetime
from pymongo import MongoClient

MONGO_URL = 'mongodb+srv://user_imt:2020@s5resumesdb-ppukj.azure.mongodb.net/test'

class TrackingExecution:
    
    def __init__(self,collection,analysis_type,execution_dict, inputs, outputs):

        self.collection=collection
        self.analysis_type=analysis_type
        self.execution_dict=execution_dict
        self.inputs=inputs
        self.outputs=outputs

        self.datetime_object = datetime.datetime.now()
        return
    
    def storeExecutionOneToOne(self):
        dict_cv = {
                'id' : self.inputs[0],
                'skills_match': self.outputs[0]['skills_match'],
                'domain_skills_match': self.outputs[0]['domain_skills_match'],
                'culture_match': self.outputs[0]['culture_match'],
                'required_skill_match': self.outputs[0]['required_skill_match'],
                'string_education_match': self.outputs[0]['string_education_match'],
                'explained_culture_match': self.outputs[0]['explained_culture_match']
                }
        new_execution = {
            'date_execution' : self.datetime_object,
            'analisys_type' : self.execution_dict['name'],
            'id_job' : self.inputs[1],            
            'cvs_evaluated' : dict_cv
            }
        self.collection.insert_one(new_execution)
        print("execution stored")
        return 

    def storeExecutionManyToOne(self):
        #set output data: scores_by_section, score_mr_sort
        input_cvs=[]

        for i in range(len(self.inputs[0])):
            dict_cv = {
                'id' : self.outputs[1].index[i],
                'domain_skills_match' : self.outputs[1]['domain_skills_match'][i],
                'skills_match' : self.outputs[1]['skills_match'][i],
                'required_skill_match' : self.outputs[1]['required_skill_match'][i],
                'culture_match' : self.outputs[1]['culture_match'][i],
                'MRValues' : self.outputs[1]['MRValues'][i]
                #'education_match': self.outputs[1]['education_match'][i] why education is not working?
                }
            input_cvs.append(dict_cv)

        new_execution = {
            'date_execution' : self.datetime_object,
            'analisys_type' : self.execution_dict['name'],
            'id_job' : self.inputs[1],
            'cvs_evaluated' : input_cvs
            }
        self.collection.insert_one(new_execution)
        print("execution stored")
        return 
    
    def storeExecution(self):
        #creating cvs dictionary
        #Candidates ID are always input[0] -> this can be a list or a unique value
        #Job Post ID is always input[1] -> this is always a unique value
        #There exist different outputs, depending on the type of analysis. There exist an analysis_axes value for ManyToOneMatching
        #but not for OneToOneMatching.
        #domain_skills_match, skills_match, required_skill_match, culture_match are always similar we will use this variables 
        # as score.
        if (self.analysis_type==0): self.storeExecutionOneToOne()
        else: self.storeExecutionManyToOne()
        return