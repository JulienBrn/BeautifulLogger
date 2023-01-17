import logging
import termcolor

class BeautifulFormatter(logging.Formatter):

    mformat = "[{asctime}] {coloredlevel} @ {filename}:{lineno:<4d}: {message}"

    colors = {
        "DEBUG" : ("grey", ""),
        "INFO"  : ("green", ""),
        "WARNING"  : ("green", "on_yellow"),
        "ERROR"  : ("green", "on_red"),
        "CRITICAL"  : ("white", "on_red"),
    }

    def get_colored_level(self, level, levelname) :
        if(levelname in self.colors) :
            (fontc, backc) = self.colors[levelname]
            if(fontc!="" and backc!=""):
                return termcolor.colored(" {:8s} ".format(levelname), fontc, backc)
            elif(fontc!=""):
                return termcolor.colored(" {:8s} ".format(levelname), fontc)
            else:
                return termcolor.colored(" {:8s} ".format(levelname), backc)
        else:
            return " {:8s} ".format(levelname)
            
    def format(self, record):
        record.coloredlevel=self.get_colored_level(record.levelno, record.levelname) 
        formatter = logging.Formatter(self.mformat, style='{')
        return formatter.format(record)

def make_beautiful(handler : logging.Handler) -> None:
    handler.setFormatter(BeautifulFormatter())