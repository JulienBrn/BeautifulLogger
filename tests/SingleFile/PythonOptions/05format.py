import logging
import beautifullogger

### Configuration ####
beautifullogger.setup(displayFormat="[{asctime}] {colorama}{levelname:^8s} @{name}{reset} {filename}:{lineno:<4d}: {message}")

### Declaring logger for this module
logger = logging.getLogger(__name__)

### Displaying Test (i.e. calls logger.debug, logger.info, logger.warning, logger.error and error.critical)
beautifullogger.test(logger)