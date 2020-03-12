

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

    def getJobEducation(self,JsonObject):
        job_education ={}
        count = len(JsonObject['SovrenData']['Education']['Degree'])
        for i in range(0,count):
            job_education['DegreeName'] = JsonObject['SovrenData']['Education']['Degree'][i]
        return job_education
