import logging

# Creates a root logger with our suggested default configuration. 
# The configuration logs all messages (level = 0) to file "log.txt" (appends to it) in a nice format
logging.basicConfig(level=0, filename="log.txt", filemode="a", format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s @ %(filename)s:%(lineno)s')
logging.info("New Run Start")


# Function used for testing
i=0

def print_test_messages(logger : logging.Logger):
    global i
    print("Printing number {}".format(i))
    logger.debug("Printing number {}".format(i))
    i=i+1
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")
    print("")


# Printing number 0 using default configuration
# No messages are displayed on terminal but are logged in log.txt
# This behavior can be changed by adding a handler, but this is not how we suggest to do it.
print_test_messages(logging.getLogger())

# Our suggestion : the "root" logger (created by defaultConfig) logs everything in the file log.txt
# We add a logger per file which prints logs that we fill are relevant for our module (in terminal). We use the name of the module as name of the logger.

logger = logging.getLogger(__name__)

# Let us try a print (Printing number 1).
# Notice that messages are logged in log.txt. This is because all loggers propagate messages to the root logger by default.
# However, nothing is displayed in terminal...
print_test_messages(logger)

# Let us add a handler to our logger to display in terminal 
logger_handler = logging.StreamHandler()
logger.addHandler(logger_handler)

# Let us try again (Printing number 2). This time messages are displayed in terminal and in file "log.txt"
print_test_messages(logger)

# Now that we can have almost the same behavior by using debug/info/warning/error/critical than we would have with a print (with the bonus of logging to "log.txt")
# Let us see a few advantages
# First, we can dismiss messages under a certain level for each logger separately. 
# In a real setup, this means we can enable DEBUG messages for some modules and disable them for others
# Or more simply, instead of erasing info/debug prints from the code when they are not necessary, we can simply change the "level" of the logger_handler
# Note that this is different from changing the level of the logger with logger.setLevel(). Try it and the difference can be seen in log.txt
logger_handler.setLevel(logging.WARNING)
print_test_messages(logger)

# We can also change the display of the logger. 
# I created a simple package "beautifullogger", installable with "pip install beautifullogger" that shows an example
# Once you get used to logging, feel free to use your own beautiful formatter
import beautifullogger
beautifullogger.make_beautiful(logger_handler) #Or logger.handlers[0]
print_test_messages(logger)

# Let us just show how they are all displayed by resetting the level
logger_handler.setLevel(logging.DEBUG)
print_test_messages(logger)