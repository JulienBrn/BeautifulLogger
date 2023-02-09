import logging
import beautifullogger

beautifullogger.setup(configFile="https://raw.githubusercontent.com/JulienBrn/BeautifulLogger/main/themes/pycharm.json")
logger=logging.getLogger(__name__)

logger.debug("test debug")
logger.info("test info")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")