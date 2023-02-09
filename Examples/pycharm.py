import logging
import beautifullogger

beautifullogger.setup(configFile="themes/pycharm.json")
logger=logging.getLogger(__name__)

logger.debug("test debug")
logger.info("test info")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")