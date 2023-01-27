# BeautifulLogger

**WARNING** Version 3.0 made a complete overhaul of the code. Documentation and examples are not yet fully updated and you may see some issues. 

A beautiful default configuration for Python loggers. 

Note: improved error messages for invalid configurations should come in the next version.

## Goals :
1. Show that loggers are better than prints :
    - Just as simple to use
    - Naturally sets different types of messages : info, warning, error, ...
    - Can contain extra information
    - Can save information to files
    - You can change display/information **without modifying the original code**
2. Provide simple default logger setup which shows the benefits (coloring, log file, progress bars, ...). 
3. The setup is optional and can be easily changed **without modifying the original code** so that you do not depend on *BeautifulLogger*


## Installation

Simply use `pip install beautifullogger`

## Usage

Most of the usage comes from correctly using the [logging](https://docs.python.org/3/library/logging.html) python module.
Here we describe what we believe is appropriate for beginners.

### Basic single file usage -[Example](https://github.com/JulienBrn/BeautifulLogger/blob/main/Examples/simple_usage.py)-

A simple use case is when one uses only a single file (view this [example](https://github.com/JulienBrn/BeautifulLogger/blob/main/Examples/simple_usage.py)).
In that case, do the following:

1. `import logging`
2. `import beautifullogger`
3. `beautifullogger.setup(named_params)`.  If you do not specify any parameters (default configuration), logging output is displayed with colors to your terminal and is also logged in a file named log.txt. Parameters will be discussed latter on.
4. `logger = logging.getLogger(__name__)`. This creates a logger with name "__main__" (the relevance of this will be seen latter).
5. Setup the messages you wish to see with `beautifullogger.setDisplayLevel(logging.INFO)` (for example). See [setLevel](https://docs.python.org/3/library/logging.html#logging.Logger.setLevel) for more information. Note that this only changes the messages that are displayed. All messages are still logged to log.txt.
6. Then use the following functions to log messages:
    - `logger.debug(msg)` : for messages to help you debug your code
    - `logger.info(msg)` : for messages that displays info to the user such as progress, extra information of loaded files, ...
    - `logger.warning(msg)` : for messages that displays information suggesting that things may not go as expected
    - `logger.error(msg)` : for error messages stating that something went wrong
    - `logger.critical(msg)` : for error messages from which you can not recover and the application needs to be stopped

Note that the code mainly uses the logging library and the dependancy on *BeautifulLogger* is only for the setup (which can be replaced by [logging.basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig) or even more advanced options).

### Basic several file usage -[Example](https://github.com/JulienBrn/BeautifulLogger/blob/main/Examples/complex_usage.py)-

Let us distinguish 2 types of files :

1. The "main" file (i.e. the one on which the python interpreter is called). In our example, [complex_usage.py](https://github.com/JulienBrn/BeautifulLogger/blob/main/Examples/complex_usage.py)
2. The support files (i.e. the ones that are imported). In our example [support.py](https://github.com/JulienBrn/BeautifulLogger/blob/main/Examples/support.py)

The basic usage is the following:
1. In the "main" file, write code as in *Basic one file usage*. Additional possibilities are available and will be discussed in the next section.
2. In the support files, we do not use *BeautifulLogger* and only use the python [logging](https://docs.python.org/3/library/logging.html) module:
    1. `import logging`
    2. `logger = logging.getLogger(__name__)`. This creates a logger with same name as the current file.
    3. Then use the previous 5 functions to log messages (debug, info, ...).
     Note that we did not use setLevel before this step because we are in a support file.

### Logging progress bars

Documentation to come. Principle : you log with the normal logging module and add a progress information. If used without beautiful logger, the normal message is displayed. However, when using BeautifulLogger the extra information is processed to display progress bars instead of the logging message.

 Examples:

 1. `logger.info("Test progressed by 20 out of 20 000 files", extra={"progress":{"counter" : "Test" , "update": 20, "max" : 20000, "unit" : "files"}})`
 2. `logger.info("Temp2 progressed by 20 out of 20 000 files", extra={"progress":{"counter":"  Temp2", "update": 20, "max" : 600, "auto-rm" : True}})`

### Modifying loggers from imported files/modules

Documentation to come. Does not depend on *BeautifulLogger*  and a basic principle is shown in [complex_usage.py](https://github.com/JulienBrn/BeautifulLogger/blob/main/Examples/complex_usage.py)

## Custumizing your logger

### setup parameters

Proper documentation to come. For now, the default parameters and their values are listed below. Note: an additional "configFile" parameter can be provided and allows to set up options in a json text file. Note that colors are based on the colorama module.

```Python
"displayLevel" : 0, 
"displayFormat" : "[{asctime}] {colorama}{levelname:^8s}{reset} @{name} {filename}:{lineno:<4d}: {message}",
"logfile" : "log.txt", "logmode" : "a",
"logformat" : "[{asctime}] {levelname} @{name} {filename}:{lineno:<4d}: {message}",
"style" : {"DEBUG" : "", "INFO" : "Fore.GREEN", "WARNING" : "Back.YELLOW", "ERROR" : ["Back.RED", "Fore.WHITE"], "CRITICAL" : ["Back.RED", "Fore.WHITE", "Style.BRIGHT"] },
```   

### Other functions

Documentation to come.

## Implementation in relation to the logging module (useful for more advanced usage)

Documentation to come. 
<!-- Relevant functions are `beautifullogger.setColor` and `beautifullogger.addLevel`. -->








<!-- 
This creates a default setup where logs are written to file logname in mode logmode. Default is "log.txt" and "a" (for append to file). This replaces the call to [logging.basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig) and works similarly.   
Colors are set by the theme. The theme variable can either be set to a local file or to a url. Examples of themes are available in the [themes](https://github.com/JulienBrn/BeautifulLogger/tree/main/themes) folder. Note that you cannot use the github url directly to load them and should use the rawgithub url instead. For example: [https://cdn.githubraw.com/JulienBrn/BeautifulLogger/main/themes/pycharm.json](https://cdn.githubraw.com/JulienBrn/BeautifulLogger/main/themes/pycharm.json).  
To create your own colors, you should be aware that colors and attributes are then fed to [termcolor](https://pypi.org/project/termcolor/), but not all configurations are supported by all terminals. To view what is supported in your terminal and how it is displayed, you may use the [testcolors script](https://github.com/JulienBrn/BeautifulLogger/blob/main/tests/testcolors.py). -->