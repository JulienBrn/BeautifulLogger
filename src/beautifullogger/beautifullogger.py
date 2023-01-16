import logging
import termcolor

class BeautifulFormatter(logging.Formatter):

    mformat = "[{asctime}] {coloredlevel} @ {filename}:{lineno:<4d}: {message}"

    def get_colored_level(self, level, levelname) :
        if(level <= logging.DEBUG):
            return termcolor.colored(" {:8s} ".format(levelname), "grey")
        elif(level <= logging.INFO):
            return termcolor.colored(" {:8s} ".format(levelname), "green")
        elif(level <= logging.WARNING):
            return termcolor.colored(" {:8s} ".format(levelname), "green", "on_yellow")
        elif(level <= logging.ERROR):
            return termcolor.colored(" {:8s} ".format(levelname), "green", "on_red")
        elif(level <= logging.CRITICAL):
            return termcolor.colored(" {:8s} ".format(levelname), "white", "on_red")

    def format(self, record):
        record.coloredlevel=self.get_colored_level(record.levelno, record.levelname) 
        formatter = logging.Formatter(self.mformat, style='{')
        return formatter.format(record)

def make_beautiful(handler : logging.Handler) -> None:
    handler.setFormatter(BeautifulFormatter())