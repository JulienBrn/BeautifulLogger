import logging
import termcolor
import sys
import json
import requests
import pathlib

class BeautifulFormatter(logging.Formatter):

    mformat = "[{asctime}] {coloredlevel} @{name} {filename}:{lineno:<4d}: {message}"

    colors = {
        logging.DEBUG : ["grey", "", []],
        logging.INFO  : ["green", "", []],
        logging.WARNING  : ["green", "on_yellow", []],
        logging.ERROR  : ["green", "on_red", []],
        logging.CRITICAL  : ["white", "on_red", ["bold"]],
    }

    def get_colored_level(self, level, levelname) :
        if(level in self.colors) :
            [fontc, backc, attrs] = self.colors[level]
            if(fontc!="" and backc!=""):
                return termcolor.colored(" {:8s} ".format(levelname), fontc, backc, attrs=attrs)
            elif(fontc!=""):
                return termcolor.colored(" {:8s} ".format(levelname), fontc, attrs=attrs)
            elif(backc!=""):
                return termcolor.colored(" {:8s} ".format(levelname), backc, attrs=attrs)
            elif(attrs!=[]):
                return termcolor.colored(" {:8s} ".format(levelname), attrs=attrs)
            else:
                return " {:8s} ".format(levelname)
        else:
            return " {:8s} ".format(levelname)

    def format(self, record):
        record.coloredlevel=self.get_colored_level(record.levelno, record.levelname) 
        formatter = logging.Formatter(self.mformat, style='{')
        return formatter.format(record)



def make_beautiful(handler : logging.Handler) -> None:
    handler.setFormatter(BeautifulFormatter())


def setup_beautiful_logging(logfile:str ="log.txt", logmode:str ="a", theme=""):
    rootLogger = logging.getLogger()
    rootLogger.setLevel(0)
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    log_handler = logging.FileHandler(filename = logfile, mode = logmode)
    log_handler.setLevel(0)
    stderr_handler.setLevel(0)
    log_handler.formatter=logging.Formatter("[{asctime}] {levelname} @{name} {filename}:{lineno:<4d}: {message}", style='{')
    make_beautiful(stderr_handler)
    try:
        if(theme!=""):
            if(not pathlib.Path(theme).exists()):
                colordict=json.loads(requests.get(theme).text)
            else:
                with open(theme) as user_file:
                    colordict = json.loads(user_file.read())
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
            stderr_handler.formatter.colors = {levelmap[name]: val for name, val in colordict.items()}
    except BaseException as e:
        raise BaseException("Impossible to load theme, error is {}".format(e))

    rootLogger.addHandler(stderr_handler)
    rootLogger.addHandler(log_handler)

def addLevel(level, levelname, font_color="", background_color="", attrs=[]):
    stderr_handler=logging.getLogger().handlers[0]
    logging.addLevelName(level, levelname.upper())
    stderr_handler.formatter.colors[level]=[font_color, background_color, attrs]

    def writeLog(self, msg):
        self.log(level, msg)

    setattr(logging.Logger, levelname.lower(), writeLog)

def setColor(level, font_color="", background_color="", attrs=[]):
    stderr_handler=logging.getLogger().handlers[0]
    stderr_handler.formatter.colors[level]=[font_color, background_color, attrs]