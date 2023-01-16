import logging

logging.basicConfig(level=0, filename="log.txt", filemode="a", format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s @ %(filename)s:%(lineno)s')
logging.info("New Run Start")
logger = logging.getLogger(__name__)
logger_handler = logging.StreamHandler()
logger.addHandler(logger_handler)
import beautifullogger #Module I created for nice formatting
beautifullogger.make_beautiful(logger_handler) #Optional, used for nicer formatting
logger_handler.setLevel(logging.DEBUG) #Or logging.WARNING, logging.ERROR, ...


#My code
import pathlib
file = pathlib.Path("test.txt")
logger.info("Attempting to open file {}".format(file))
if(not file.exists()) :
    logger.error("File {} does not exist".format(file))
else :
    logger.info("File {} found".format(file))
    #Your code
    pass