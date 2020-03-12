

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