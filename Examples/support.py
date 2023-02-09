import logging

logger=logging.getLogger(__name__)

def show():
    logger.debug("support test debug")
    logger.info("support test info")
    logger.warning("support test warning")
    logger.error("support test error")
    logger.critical("support test critical")