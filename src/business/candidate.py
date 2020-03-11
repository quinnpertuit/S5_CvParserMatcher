from services.data_extraction.candidate.candidate import CandidateDataExtraction

class CandidateBusiness:
    def __init__(self,file):
        self.file = file

    def upload(self,file):
        #parseTheresume
        #insertIntoDatabase
        Candidate_data_extraction = CandidateDataExtraction(file)
        experience_descritpion = Candidate_data_extraction.getCandidateExperience(file)
        print(experience_descritpion)
        return experience_descritpion

