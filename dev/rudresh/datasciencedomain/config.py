import configparser
import os



class Config:
    """ A simple abstraction layer for the configuration file """
     
    def __init__(self, paper = None):
        """ Initialising the config class
        """
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.config_file = os.path.join(self.dir, "config.ini")
        self.config = configparser.ConfigParser()
        self.read_config_file()
    
# =============================================================================
#     ONTOLOGY
# =============================================================================
    def get_cso_path(self):
        """ Returns the path of the local version of CSO """
        return os.path.join(self.dir, self.config['ontology']['cso_path'])
    
    def get_cso_pickle_path(self):
        """ Returns the path of the local pickle version of CSO """
        return os.path.join(self.dir, self.config['ontology']['cso_pickle_path'])
    

# =============================================================================
#     MODEL  
# =============================================================================
    
    def get_cached_model(self):
        """ Returns the local path of the cached model """
        return os.path.join(self.dir, self.config['model']['cached_model'])
# =============================================================================
#     READ CONFIG FILE
# =============================================================================
    def read_config_file(self):
        """ Reads the config file """
        self.config.read(self.config_file)
        