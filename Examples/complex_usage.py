import support
import logging
import beautifullogger

beautifullogger.setup_beautiful_logging()
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug("test debug")
logger.info("test info")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")


support.show()

loggersupport=logging.getLogger("support")
loggersupport.setLevel(logging.WARNING)

support.show()

logger.debug("test debug")
logger.info("test info")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")

