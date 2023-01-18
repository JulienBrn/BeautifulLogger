import logging

logger=logging.getLogger(__name__)

def show():
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")