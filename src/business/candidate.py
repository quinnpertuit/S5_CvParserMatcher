from services.data_extraction.candidate.candidate import CandidateDataExtraction
from services.data_processing.candidate_processing.candidate import CandidateDataProcessing
import services.graph_treat as gt
import services.lang_processing as lp

class CandidateBusiness:
    def __init__(self,file):
        self.file = file

    def upload(self,file):

        #below functionality has to be done by moises
        #parseTheresume
        #insertIntoDatabase
        Candidate_data_extraction = CandidateDataExtraction(file)
        experience_description = Candidate_data_extraction.getCandidateExperience(file)
        return experience_description

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



