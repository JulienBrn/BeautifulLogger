import logging
import beautifullogger


### Configuration ####
beautifullogger.setup(logfile="logtest3.txt")
beautifullogger.setDisplayLevel(logging.WARNING)

### Declaring logger for this module
logger = logging.getLogger(__name__)

### Displaying Test
beautifullogger.test(logger)