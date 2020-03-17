from bson.objectid import ObjectId
import services.helpers as hp

class JobDataExtraction:
    def __init__(self,JobJson):
        # generateIDnumber automatically
        self.JobJson = JobJson

    def parseTheJob(self,document):
        #call the api and parse the Cv
        return

    def insertIntoDatabase(self,JsonObject):
        return

    def getJobExperience(self,JsonObject):
        # JobDescription = ''
        JobDescription = JsonObject['SovrenData']['SourceText']
        return JobDescription

    def getSourceText(self, jp:list):
        return [ self.getJobExperience(json) for json in jp ]

    def getJobPostString(self, job_coll, n:int=1, o_id:ObjectId=None):
        job_posts = job_coll.find(limit=n) if not o_id else [job_coll.find_one({ '_id': o_id if not isinstance(o_id, str) else ObjectId(o_id) })]
        job_posts = list(job_posts)
        sources_string = " ".join(self.getSourceText(job_posts))
        return sources_string
        
    def getJobEducation(self,JsonObject):
        job_education ={}
        count = len(JsonObject['SovrenData']['Education']['Degree'])
        for i in range(0,count):
            job_education['DegreeName'] = JsonObject['SovrenData']['Education']['Degree'][i]
        return job_education

    def getJobPostSkill(self ,jsonTaxanomy, Required = False):
        skill = []
        for i in range(0,len(jsonTaxanomy)):
            for j in range(0,len(jsonTaxanomy['Subtaxonomy'][i]['Skill'])):
                dictSkill = jsonTaxanomy['Subtaxonomy'][i]['Skill'][j]
                if dictSkill["@existsInText"]== True and dictSkill["@required"]== Required:
                    skill.append(dictSkill['@name'])
                if "ChildSkill" in  dictSkill.keys() and dictSkill["ChildSkill"][0]["@existsInText"]== True and dictSkill["ChildSkill"][0]["@required"]== Required:
                    skill.append(dictSkill["ChildSkill"][0]['@name'])
        return skill

