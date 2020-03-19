from services.data_extraction.job_post.jobpost import JobDataExtraction
from services.data_processing.job_post_processing.jobpost import JobDataProcessing
import services.graph_treat as gt


class JobPostBusiness:
    def __init__(self,file):
        self.file = file

    def download(self,file):
        #below functionality has to be done by mosies
        #parseTheresume
        #insertIntoDatabase
        Job_data_extraction = JobDataExtraction(file)
        experience_description = Job_data_extraction.getJobExperience(file)
        job_education_dict = Job_data_extraction.getJobEducation(file)
        return experience_description,job_education_dict


    def getJobSkillDict(self,exp_description):
        job_data_processing = JobDataProcessing(exp_description)
        job_skill_dict = job_data_processing.getSkillOntoloies(exp_description)
        job_domain_skill_dict = job_data_processing.getDataScienceSkillOntoloies(exp_description)
        return job_skill_dict,job_domain_skill_dict

    def getJobSkillGraph(self,job_skill_dict):
        job_data_processing = JobDataProcessing(job_skill_dict)
        skill_edges = job_data_processing.generate_edges(job_skill_dict['explanation'])
        return job_data_processing.generateSkillGraph(skill_edges)


    def getJobPostCultureEvaluatedGraph(self, candidate_id, graph_path, model, job_coll):
        G = gt.loadGraphFromFile(graph_path)
        jpde = JobDataExtraction(None)
        jp_string = jpde.getJobPostString(job_coll, o_id=candidate_id)
        _ = gt.stringToCultureGraph(G, model, jp_string)
        return G
    
    def getJobEducationDegree(self, job_education_dict):
        job_data_processing = JobDataProcessing(job_education_dict)
        return job_data_processing.getNormalizedDegreeEducation(job_education_dict) 


    def getJobRequiredSkill(self, file):
        job_data_processing = JobDataProcessing(file)
        required_skill =  job_data_processing.getJobSkills(file)
        return required_skill['requiredSkill']


    def getJobDesiredSkill(self, file):
        job_data_processing = JobDataProcessing(file)
        required_skill =  job_data_processing.getJobSkills(file)
        return required_skill['desiredSkill']