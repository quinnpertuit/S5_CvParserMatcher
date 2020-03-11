    
class CandidateDataExtraction:

    def __init__(self,CandidateJson):
        # generateIDnumber automatically
        self.CandidateJson = CandidateJson
    
    def parseTheresume(self,document):
        #call the api and parse the Cv
        return

    def insertIntoDatabase(self,JsonObject):
        return

        
    #candidate_id
    #for the moment we are not fetching the experience from database

    def getCandidateExperience(self,CandidateJson):
        JobDescription = ''
        count = len(CandidateJson['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg'])
        for i in range(0,count):
            JobDescription += CandidateJson['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg'][i]['PositionHistory'][0]['Description']
        return JobDescription
