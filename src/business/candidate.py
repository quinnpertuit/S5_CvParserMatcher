from services.data_extraction.candidate.candidate import CandidateDataExtraction
from services.data_processing.candidate_processing.candidate import CandidateDataProcessing
import services.graph_treat as gt
import services.lang_processing as lp


class CandidateBusiness:
    def __init__(self,file):
        self.file = file

    def upload(self,file):

        #below functionality has to be done by mosies
        #parseTheresume
        #insertIntoDatabase
        Candidate_data_extraction = CandidateDataExtraction(file)
        experience_description = Candidate_data_extraction.getCandidateExperience(file)
        candidate_education_dict = Candidate_data_extraction.getCandidateEducation(file)
        return experience_description, candidate_education_dict

    def getCandidateSkillGraph(self,exp_description):
        Candidate_data_processing = CandidateDataProcessing(exp_description)
        Candidate_skill_dict = Candidate_data_processing.getSkillOntoloies(exp_description)
        skill_edges = Candidate_data_processing.generate_edges(Candidate_skill_dict['explanation'])

        return Candidate_data_processing.generateSkillGraph(skill_edges)

    def getCandidateCultureEvaluatedGraph(self, candidate_id, graph_path, model, db_col):
        G = gt.loadGraphFromFile(graph_path)
        cde = CandidateDataExtraction(None)
        cv_string = cde.getResumeString(db_col, o_id=candidate_id)
        _ = gt.stringToCultureGraph(G, model, cv_string)
        return G
        
    def getCandidateEducationDegree(self, candidate_education_dict):
        Candidate_data_processing = CandidateDataProcessing(candidate_education_dict)
        return Candidate_data_processing.getNormalizedDegreeEducation(candidate_education_dict)





