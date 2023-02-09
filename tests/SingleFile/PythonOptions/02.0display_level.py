import logging
import beautifullogger


### Configuration ####
beautifullogger.setup(displayLevel=logging.WARNING)

### Declaring logger for this module
logger = logging.getLogger(__name__)

### Displaying Test (i.e. calls logger.debug, logger.info, logger.warning, logger.error and error.critical)
beautifullogger.test(logger)
beautifullogger.setDisplayLevel(0)
beautifullogger.test(logger)