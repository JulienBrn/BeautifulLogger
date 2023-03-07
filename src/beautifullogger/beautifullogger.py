import logging
import sys
import json
import requests
import pathlib
from typing import List, Dict, TypeVar, Union

__docformat__ = "google"

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
    
def get_level(name: Union[int,str]):
    if isinstance(name, int):
        return name
    try:
        return levelmap[name]
    except KeyError:
        logger.error("Unable to find level {}. Defaulting to 0.".format(name))
        return 0

def get(str: str):
    try:
        if "Fore." in str:
            return vars(colorama.Fore)[str[5:]]
        elif "Back." in str:
            return vars(colorama.Back)[str[5:]]
        elif "Style." in str:
             return vars(colorama.Style)[str[6:]]
        elif str == "":
            return ""
        else:
            logger.warning("Unrecognized style option {}. Continuing without this styling".format(str))
            return ""
    except:
        logger.warning("Unrecognized style option {}. Continuing without this styling".format(str))
        return ""

class __opt:
    def __init__(self, val):
        self.val=val
        
    def __repr__ (self):
        return "__opt({})".format(self.val)
    def __str__ (self):
        return "{}".format(self.val)
    
S = TypeVar('S')  
Opt = Union[S , __opt]

import inspect 

def setup(
    displayLevel: Opt[int] = __opt(0), 
    logformat: str = __opt("[{asctime}] {levelname:^8s} @{name} {filename}:{lineno:<4d}: {message}"),
    displayFormat: str = __opt("[{asctime}] {colorama}{levelname:^8s}{reset} @{name} {filename}:{lineno:<4d}: {message}"), 
    logfile: str = __opt("log.txt"),
    logmode:str = __opt("a"),
    style: Dict[int, Union[str, List[str]]] = __opt({
        logging.DEBUG : "", 
        logging.INFO : "Fore.GREEN", 
        logging.WARNING : "Back.YELLOW", 
        logging.ERROR : ["Back.RED", "Fore.WHITE"], 
        logging.CRITICAL : ["Back.RED", "Fore.WHITE", "Style.BRIGHT"]
    }),
    configFile: str = __opt(None)
):
    """
        Do not worry about __opt, it is only to determine whether the argument was passed
        Args:
            displayLevel: An open smalltable.Table instance.
            logformat: A sequence of strings representing the key of each table
            row to fetch.  String keys will be UTF-8 encoded.
            displayFormat: If True only rows with values set for all keys will be
            returned.
    """
    if logging.getLogger().handlers ==[]:
        logging.basicConfig(format="[{asctime}] {levelname:^8s} @{name} {filename}:{lineno:<4d}: {message}", style='{')
    if not logger.level:
        logger.setLevel(logging.WARNING)
    params=locals()
    paramConfig={k:v for k,v in params.items() if not isinstance(v, __opt)}
    
    signature = inspect.signature(setup)
    defaultConfig={n:p.default.val for n,p in signature.parameters.items()}
    
    config={}
    try:
        if "configFile" in paramConfig:
            configFile=paramConfig["configFile"]
            logger.debug("Loading Logger Config from {}".format(configFile))
            if not pathlib.Path(configFile).exists():
                logger.debug("Config file {} not found on local file system. Treating {} as an url.".format(configFile, configFile))
                response = requests.get(configFile)
                if not response.ok:
                    raise ConnectionError("Impossible to download contents of {}. Response is {}", response)
                config=json.loads(response.text)
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

    color_dict = {get_level(name): mget(val) for name, val in newConfig["style"].items()}

    logger.debug("Color dict is {}".format(color_dict))
    logging.getLogger().handlers=[]
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
