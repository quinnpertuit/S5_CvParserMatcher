from services.data_extraction.job_post.jobpost import JobDataExtraction

from services.data_processing.job_post_processing.jobpost import JobDataProcessing


class JobPostBusiness:
    def __init__(self,file):
        self.file = file

    def upload(self,file):

        #below functionality has to be done by mosies
        #parseTheresume
        #insertIntoDatabase
        Job_data_extraction = JobDataExtraction(file)
        experience_description = Job_data_extraction.getJobExperience(file)
        return experience_description

    def getJobSkillGraph(self,exp_description):
        job_data_processing = JobDataProcessing(exp_description)
        job_skill_dict = job_data_processing.getSkillOntoloies(exp_description)
        skill_edges = job_data_processing.generate_edges(job_skill_dict['explanation'])
        return job_data_processing.generateSkillGraph(skill_edges)
