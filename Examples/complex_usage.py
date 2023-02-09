import support
import logging
import beautifullogger
import colorama

beautifullogger.setup()
logger=logging.getLogger(__name__)

logger.debug("test debug")
logger.info("test info")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")

logger.info("Now calling support function", extra={"colorama":colorama.Back.CYAN})
support.show()

logger.info("Now hiding information that are not warnings or above. They can still be found in log.txt", extra={"colorama":colorama.Back.CYAN})
beautifullogger.setDisplayLevel(logging.WARNING)

logger.debug("test debug")
logger.info("test info")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")


support.show()

beautifullogger.setDisplayLevel(0)
logger.info("Now resetting what can be seen but hiding only under warnings for the support logger (this disables it in log.txt as well)", extra={"colorama":colorama.Back.CYAN})
loggersupport=logging.getLogger("support")
loggersupport.setLevel(logging.WARNING)

logger.info("In current logger", extra={"colorama":colorama.Back.CYAN})

logger.debug("test debug")
logger.info("test info")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")

logger.info("For support logger", extra={"colorama":colorama.Back.CYAN})
support.show()



