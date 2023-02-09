import logging
# import termcolor
import sys
import json
import requests
import pathlib
import enlighten

logger=logging.getLogger(__name__)

###The logger we modify#####
rootLogger=logging.getLogger()


###Handling Log File#####

# Private
log_handler = ()

# Private
def makeLogHandler(logfile:str ="log.txt", logmode:str ="a", level=0, format="[{asctime}] {levelname} @{name} {filename}:{lineno:<4d}: {message}", style='{'):
    global log_handler
    log_handler = logging.FileHandler(filename = logfile, mode = logmode)
    log_handler.setLevel(level)
    log_handler.formatter=logging.Formatter(fmt=format, style=style)

# Public
def getLogHandler():
    global log_handler
    return log_handler

###Coloring#####

import colorama
colorama.init()

color_dict = {}

class colorFilter(logging.Filter):
    def setColor(self, record):
        if record.levelno in color_dict:
            return color_dict[record.levelno]
        else:
            logger.warning("Color for level {}({}) is not set".format(record.levelno, record.levelname))
            return ""

    def filter(self, record):
        if not hasattr(record, "colorama"):
            record.colorama = self.setColor(record)
        if not hasattr(record, "reset"):
            record.reset = colorama.Style.RESET_ALL
        return 1
    
### Seting Stderr formatter

stderr_handler = ()
def makeStderrHandler(level=0, format="[{asctime}] {colorama}{levelname:^8s}{reset} @{name} {filename}:{lineno:<4d}: {message}", style='{'):
    global stderr_handler, bfilter
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(level)
    stderr_handler.formatter=logging.Formatter(fmt = format, style=style)
    stderr_handler.addFilter(colorFilter())

def getStderrHandler():
    global stderr_handler
    return stderr_handler

def setDisplayLevel(level):
    global stderr_handler
    stderr_handler.setLevel(level)


###Setup###


defaultConfig={
        "displayLevel" : 0, 
        "displayFormat" : "[{asctime}] {colorama}{levelname:^8s}{reset} @{name} {filename}:{lineno:<4d}: {message}",
        "logfile" : "log.txt", "logmode" : "a",
        "logformat" : "[{asctime}] {levelname} @{name} {filename}:{lineno:<4d}: {message}",
        "style" : {"DEBUG" : "", "INFO" : "Fore.GREEN", "WARNING" : "Back.YELLOW", "ERROR" : ["Back.RED", "Fore.WHITE"], "CRITICAL" : ["Back.RED", "Fore.WHITE", "Style.BRIGHT"] },
    }

try:
    levelmap=logging.getLevelNamesMapping()
except:
    levelmap={
        "DEBUG" : 10,
        "INFO" : 20,
        "WARNING" : 30,
        "ERROR" : 40,
        "CRITICAL" : 50
    }

def get(str: str):
    try:
        if "Fore." in str:
            return vars(colorama.Fore)[str[5:]]
        elif "Back." in str:
            return vars(colorama.Back)[str[5:]]
        elif "Style." in str:
             return vars(colorama.Style)[str[6:]]
        else:
            logger.warning("Unrecognized style option {}. Continuing without this styling".format(str))
            return ""
    except:
        logger.warning("Unrecognized style option {}. Continuing without this styling".format(str))
        return ""

def setup(**kwargs):
    """ Setups beautiful logging by modifying the root logger. Possible named arguments are (and default values)

        "displayLevel" : 0, 
        "displayFormat" : "[{asctime}] {colorama}{levelname:^8s}{reset} @{name} {filename}:{lineno:<4d}: {message}",
        "logfile" : "log.txt", "logmode" : "a",
        "logformat" : "[{asctime}] {levelname} @{name} {filename}:{lineno:<4d}: {message}",
        "style" : {
            "DEBUG" : "", 
            "INFO" : "Fore.GREEN", 
            "WARNING" : "Back.YELLOW", 
            "ERROR" : "Back.RED Fore.WHITE", 
            "CRITICAL" : "Back.RED + Fore.WHITE + Style.BRIGHT" 
         },
         "configFile": None
   
        If configFile is set, then additional configuration is then searched in the file or url that is specified.
    """
    global defaultConfig
    paramConfig=kwargs
    config={}
    try:
        if "configFile" in paramConfig:
            configFile=paramConfig["configFile"]
            logger.debug("Loading Logger Config from {}".format(configFile))
            if not pathlib.Path(configFile).exists():
                logger.debug("Config file {} not found on local file system. Treating {} as an url.".format(configFile, configFile))
                response = requests.get(configFile).text
                if not response.ok:
                    raise ConnectionError("Impossible to download contents of {}. Response is {}", response)
                config=json.loads()
            else:
                with open(configFile) as user_file:
                    config = json.loads(user_file.read())
            if "displayLevel" in config:
                config["displayLevel"] = int(config["displayLevel"])
            if "style" in config and not isinstance(config["style"], dict):
                logger.error("Config file {} has style key but is not of dictionary type (got {}). Ignoring that style key".format(configFile, type(config["style"])))
                del config["style"]
            logger.debug("Config file {} loaded. Got : {}".format(configFile, config))
    except BaseException as e:
        logger.error("Impossible to load config file {}. Reason : {}".format(configFile, e))

    logger.debug("Merging default configuration with parameters configuration, with configFile configuration")

    newConfig = defaultConfig.copy()
    newConfig.update(config)
    newConfig.update(paramConfig)


    newConfig["style"] = defaultConfig["style"]
    if "style" in config:
        newConfig["style"].update(config["style"])
    if "style" in paramConfig:
        newConfig["style"].update(paramConfig["style"])
    
    logger.debug("Retrieved final configuration. Got {}".format(newConfig))
    logger.debug("Creating color dictionary".format(newConfig))
    
    
    global color_dict, levelmap

    def mget(val):
        if isinstance(val, str):
            return get(val)
        else:
            return ''.join([get(v) for v in val])

    color_dict = {levelmap[name]: mget(val) for name, val in newConfig["style"].items()}

    logger.debug("Color dict is {}".format(color_dict))

    makeLogHandler(logfile=newConfig["logfile"], logmode=newConfig["logmode"], format=newConfig["logformat"])
    makeStderrHandler(level=newConfig["displayLevel"], format=newConfig["displayFormat"])
    rootLogger.addHandler(log_handler)
    rootLogger.addHandler(stderr_handler)
    rootLogger.setLevel(0)

def test(logger):
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")


if(__name__=="__main__"):
    import time 
    setup(configFile="themes/config.json")
    test(logger)
    logger.info("test", extra={"colorama": colorama.Back.GREEN + colorama.Style.BRIGHT + colorama.Fore.CYAN})
    logger.info("test")
    i=0
    while i<30:
        i=i+1
        logger.info("Progressed", extra={"colorama":colorama.Fore.BLUE})
        time.sleep(0.1)  # Simulate work
    i=0
    while i<30:
        i=i+1
        logger.info("Progressed by 20", extra={"progress":{"update": 20, "max" : 600}})
        time.sleep(0.1)  # Simulate work
    i=0
    while i<30:
        i=i+1
        logger.info("", extra={"progress":{"counter":"  Temp", "update": 20.12, "max" : 500.9, "auto-rm" : True}})
        time.sleep(0.1)  # Simulate work
    i=0
    while i<30:
        i=i+1
        logger.info("", extra={"progress":{"counter":"  Temp2", "update": 20, "max" : 600, "auto-rm" : True}})
        time.sleep(0.1)  # Simulate work
    while i<1000:
        i=i+1
        logger.info("", extra={"progress":{"counter" : "Test" , "update": 20, "max" : 20000, "unit" : "files"}})
        time.sleep(0.1)  # Simulate work