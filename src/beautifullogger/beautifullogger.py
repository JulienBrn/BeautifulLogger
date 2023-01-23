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
    log_handler.addFilter(progressFilter())

# Public
def getLogHandler():
    global log_handler
    return log_handler

class progressFilter:
    def filter(self, record):
        if hasattr(record, "progress"):
            return 0
        else:
            return 1


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


### Handling progress bars
import enlighten

class progressDisplay:

    manager=enlighten.get_manager()
    counters={}

    def_bar_format = '{desc:20}{desc_pad}{percentage:3.0f}%|{bar}| {count:{len_total}}/{total} [{elapsed}<{eta}, {rate:.2f}{unit_pad}{unit}/s]'
    def_counter_format='{desc:20}{desc_pad}{count} [{unit}{unit_pad}{elapsed}, {rate:.2f}{unit_pad}{unit}/s]{fill}'

    def filter(self, record):
        if hasattr(record, "progress"):
            if not "counter" in record.progress:
                record.progress["counter"]="Progress"
            if not record.progress["counter"] in self.counters:
                print("creating")
                self.counters[record.progress["counter"]]=self.manager.counter(desc=record.progress["counter"], bar_format=self.def_bar_format, counter_format=self.def_counter_format)
            counter = self.counters[record.progress["counter"]]
            if "max" in record.progress:
                counter.total=record.progress["max"]
            if "unit" in record.progress:
                counter.unit=record.progress["unit"]
            if "auto-rm" in record.progress:
                counter.leave=False
            updateVal = record.progress["update"] if "update" in record.progress else 1
            counter.update(updateVal)
            if counter.total and counter.count>=counter.total:
                counter.close()
                del self.counters[record.progress["counter"]]
            return 0   
        else:
            return 1

progressH = progressDisplay()
def getCounter(name:str):
    global progressH
    if name in progressH.counters:
        return progressH.counters[name]
    else:
        logger.error("Attempting to get non-existant counter {}. Counters are {}".format(name, progressH.counters))
        raise KeyError("Attempting to get non-existant counter {}. Counters are {}".format(name, progressH.counters))
    

### Seting Stderr formatter

stderr_handler = ()
def makeStderrHandler(level=0, format="[{asctime}] {colorama}{levelname:^8s}{reset} @{name} {filename}:{lineno:<4d}: {message}", style='{'):
    global stderr_handler, bfilter
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(level)
    stderr_handler.formatter=logging.Formatter(fmt = format, style=style)
    stderr_handler.addFilter(colorFilter())
    stderr_handler.addFilter(progressH)

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
        logger.info("Progressed", extra={"progress":{}})
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

# class ColoredFormatter(logging.Formatter):
#     regex = ""
#     def format(self, record : logging.record):
#         if not hasattr("color", record):
#             record.color = colorama.Fore.RED
#         if not hasattr("reset", record):
#             record.reset = colorama.Style.RESET_ALL
#         str = super().format(record)


#         if hasattr(record, "font_color") and hasattr(record, "background_color") and hasattr(record, "font_attributes"):
#             re.sub("start.*end", regex_replacement, str_input)
#             start=str.find(begin, 0)
#             while(start!=-1):
#                 end=str.find(end, start+len(start))
#                 substr = str[start+len(start):end]
#                 coloredsubstr=
#         return str

# import re
# class ColoredFormatter(logging.Formatter):
#     regex = ""
#     def format(self, record : logging.record):
#         str = super().format(record)


#         if hasattr(record, "font_color") and hasattr(record, "background_color") and hasattr(record, "font_attributes"):
#             re.sub("start.*end", regex_replacement, str_input)
#             start=str.find(begin, 0)
#             while(start!=-1):
#                 end=str.find(end, start+len(start))
#                 substr = str[start+len(start):end]
#                 coloredsubstr=
#         return str


# def colored(attr : str)

# stderr_handler = ()

# # def makeStderrHandler(colors=defaultcolors, format="[{asctime}] #BEGIN{levelname:^8s}#END @{name} {filename}:{lineno:<4d}: {message}"):
# #     global log_handler
# #     log_handler = logging.FileHandler(filename = logfile, mode = logmode)
# #     log_handler.setLevel(level)
# #     log_handler.formatter=logging.Formatter(format = format, style=style)















# class BeautifulFormatter(logging.Formatter):

#     mformat = "[{asctime}] {coloredlevel:s} @{name} {filename}:{lineno:<4d}: {message}"

#     colors = {
#         logging.DEBUG : ["grey", "", []],
#         logging.INFO  : ["green", "", []],
#         logging.WARNING  : ["green", "on_yellow", []],
#         logging.ERROR  : ["green", "on_red", []],
#         logging.CRITICAL  : ["white", "on_red", ["bold"]],
#     }

#     def get_colored_level(self, level, levelname) :
#         if(level in self.colors) :
#             [fontc, backc, attrs] = self.colors[level]
#             if(fontc!="" and backc!=""):
#                 return termcolor.colored(" {:^8s} ".format(levelname), fontc, backc, attrs=attrs)
#             elif(fontc!=""):
#                 return termcolor.colored(" {:^8s} ".format(levelname), fontc, attrs=attrs)
#             elif(backc!=""):
#                 return termcolor.colored(" {:^8s} ".format(levelname), backc, attrs=attrs)
#             elif(attrs!=[]):
#                 return termcolor.colored(" {:^8s} ".format(levelname), attrs=attrs)
#             else:
#                 return " {:8s} ".format(levelname)
#         else:
#             return " {:8s} ".format(levelname)

#     def format(self, record):
#         record.coloredlevel=self.get_colored_level(record.levelno, record.levelname) 
#         formatter = logging.Formatter(self.mformat, style='{')
#         return formatter.format(record)



# def make_beautiful(handler : logging.Handler) -> None:
#     handler.setFormatter(BeautifulFormatter())


# stderr_handler = ()
# progress_handler = ()
# manager=enlighten.get_manager()
# counters={}





# class removeProgress:
#     def filter(self, record) :
#         if hasattr(record, "progress"):
#             return 0 #Filter out record
#         else :
#             return 1 #Log record

# class handleProgress:
#     def filter(self, record) :
#         if hasattr(record, "progress"):
#             global counters, manager
#             counter_name=record.counter if hasattr(record, "counter") else "Progress"
#             max_val = record.max if hasattr(record, "max") else None
#             incr = record.incr if hasattr(record, "incr") else 1
#             if not counter_name in self.counters:
#                 self.counters[counter_name]=self.manager.counter(total=max, desc=counter_name)
#             counter = self.counters[counter_name]
#             if max_val != None:
#                 counter.total=max_val
#             counter.update(incr)
#             return 0 #Filter out record
#         else :
#             return 1 #Log record
#     pass


# def filterProgress(handler, display=True):
    
#     class ProgressFilter :
#         counters=[]
#         manager=enlighten.get_manager()
#         def __init__(self, display : bool):
#             self.display=display
#         def filter(self, record) :
#             if hasattr(record, "progress"):
#                 if(self.display):
#                     pass
#                 return 0 #Filter out record
#             else :
#                 return 1 #Log record
#         pass
#     handler.addFilter(ProgressFilter(display))




# def makeStderrHandler(theme=None, progress = ):

# def setup_beautiful_logging(logfile:str ="log.txt", logmode:str ="a", theme=""):
#     global log_handler, stderr_handler
#     rootLogger = logging.getLogger()
#     rootLogger.setLevel(0)
#     stderr_handler = logging.StreamHandler(stream=sys.stderr)
#     log_handler = logging.FileHandler(filename = logfile, mode = logmode)
#     log_handler.setLevel(0)
#     stderr_handler.setLevel(0)
#     log_handler.formatter=logging.Formatter("[{asctime}] {levelname} @{name} {filename}:{lineno:<4d}: {message}", style='{')
#     make_beautiful(stderr_handler)
#     try:
#         if(theme!=""):
#             if(not pathlib.Path(theme).exists()):
#                 colordict=json.loads(requests.get(theme).text)
#             else:
#                 with open(theme) as user_file:
#                     colordict = json.loads(user_file.read())
#             try:
#                 levelmap=logging.getLevelNamesMapping()
#             except:
#                 levelmap={
#                     "DEBUG" : 10,
#                     "INFO" : 20,
#                     "WARNING" : 30,
#                     "ERROR" : 40,
#                     "CRITICAL" : 50
#                 }
#             stderr_handler.formatter.colors = {levelmap[name]: val for name, val in colordict.items()}
#     except BaseException as e:
#         raise BaseException("Impossible to load theme, error is {}".format(e))

#     rootLogger.addHandler(stderr_handler)
#     rootLogger.addHandler(log_handler)

# def addLevel(level, levelname, font_color="", background_color="", attrs=[]):
#     global stderr_handler
#     # stderr_handler=logging.getLogger().handlers[0]
#     logging.addLevelName(level, levelname.upper())
#     stderr_handler.formatter.colors[level]=[font_color, background_color, attrs]

#     def writeLog(self, msg):
#         self.log(level, msg)

#     setattr(logging.Logger, levelname.lower(), writeLog)

# def setColor(level, font_color="", background_color="", attrs=[]):
#     global stderr_handler
#     stderr_handler.formatter.colors[level]=[font_color, background_color, attrs]