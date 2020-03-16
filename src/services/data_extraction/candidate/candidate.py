import numpy as np    
from pymongo import MongoClient
import configparser
from bson.objectid import ObjectId
import services.helpers as hp

MONGO_URL = 'mongodb+srv://user_imt:2020@s5resumesdb-ppukj.azure.mongodb.net/test'

class CandidateDataExtraction:

    def __init__(self,CandidateJson, mongoURL=MONGO_URL):
        # generateIDnumber automatically
        self.CandidateJson = CandidateJson
        self.mongoURL = mongoURL
    
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

    def buildDescriptionsList(self, resumes: list) -> dict:
        desc = np.array([])
        for res in resumes:
            orgs = res['Resume']['StructuredXMLResume']['EmploymentHistory']['EmployerOrg']
            for org in orgs:
                roles = org['PositionHistory']
                for role in roles:
                    desc = np.concatenate( (desc, [{
                    'employer': org['EmployerOrgName'],
                    'role': role['OrgName']['OrganizationName'],
                    'description': role['Description'],
                    }]))
        return desc
    
    def getSummaries(self, resumes: list) -> str:
        return [ res['Resume']['StructuredXMLResume']['ExecutiveSummary'] for res in resumes ]

    def loadResumes(self):
        client = MongoClient(self.mongoURL)
        db = client['db'] # db
        return db['resumes']

    def getDescriptionsString(self, resumes):
        desc = self.buildDescriptionsList(resumes)
        description_list = hp.getValuesOfListOfDicts(desc, 'description')
        return hp.joinArrayOfStrings(description_list)

    def getResumeString(self, db_resumes, n:int=1, o_id:ObjectId=None):
        resumes = db_resumes.find(limit=n) if not o_id else [db_resumes.find_one({ '_id': o_id if not isinstance(o_id, str) else ObjectId(o_id) })]
        resumes = list(resumes)
        summaries_string = " ".join(self.getSummaries(resumes))
        descriptions_string = self.getDescriptionsString(resumes)
        return summaries_string + " " + descriptions_string

