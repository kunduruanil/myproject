from NewsAnalysis.settings import BASE_DIR
from os.path import join
from  configparser import ConfigParser
import logging



_config=ConfigParser()

_configini = join(BASE_DIR, 'config/config.ini')

_config.read(_configini)
log_file=_config.get("files",'log')
logging.basicConfig(filename=log_file,format='%(asctime)s %(message)s')
_logger=logging.getLogger()

def clear_loggerfile(clear=False):
    if clear:
        with open(log_file, "w") as file:
            file.truncate()



'''
#help
_logger.debug("Harmless debug Message") 
_logger.info("Just an information") 
_logger.warning("Its a Warning") 
_logger.error("Did you try to divide by zero") 
_logger.critical("Internet is down") 
'''

