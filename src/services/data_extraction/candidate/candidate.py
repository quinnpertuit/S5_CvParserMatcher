    
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

    def getCandidateEducation(self,CandidateJson):
        candidate_education ={}
        count = len(CandidateJson['Resume']['StructuredXMLResume']['EducationHistory']['SchoolOrInstitution'])
        for i in range(0,count):
            candidate_education['DegreeName'] = CandidateJson['Resume']['StructuredXMLResume']['EducationHistory']['SchoolOrInstitution'][i]['Degree'][0]['DegreeName']
            candidate_education.update(CandidateJson['Resume']['StructuredXMLResume']['EducationHistory']['SchoolOrInstitution'][i]['Degree'][0]['DegreeDate'])
            candidate_education['comment'] = CandidateJson['Resume']['StructuredXMLResume']['EducationHistory']['SchoolOrInstitution'][i]['Degree'][0]['Comments']
            candidate_education['Degree'] = CandidateJson['Resume']['StructuredXMLResume']['EducationHistory']['SchoolOrInstitution'][i]['Degree'][0]['DegreeMajor'][0]['Name'][0]
        return candidate_education
