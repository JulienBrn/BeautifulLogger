import beautifullogger
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.debug("test debug")
logger.info("test info")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")


beautifullogger.make_beautiful(logger)
logger.debug("test debug")
logger.info("test info")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")