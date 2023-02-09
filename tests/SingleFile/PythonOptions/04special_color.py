import logging
import beautifullogger
import colorama

### Configuration ####
beautifullogger.setup()

### Declaring logger for this module
logger = logging.getLogger(__name__)

### Displaying Test
beautifullogger.test(logger)
logger.info("Test color", extra={"colorama":colorama.Back.GREEN + colorama.Fore.RED + colorama.Style.BRIGHT})