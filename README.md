# BeautifulLogger
A beautiful default configuration for Python loggers. 

Note: improved error messages for invalid configurations should come in the next version.

## Goals :
1. Show that loggers are better than prints :
    - Just as simple to use
    - Naturally sets different types of messages : info, warning, error, ...
    - Can contain extra information
    - Can save information to files
    - You can change display/information **without modifying the original code**
2. Provide simple default logger setup which shows the benefits (coloring, log file, ...). 
3. The setup is optional and can be easily changed **without modifying the original code** so that you do not depend on *BeautifulLogger*

This library is not addressed to advanced users of logging.

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
3. `beautifullogger.setup_beautiful_logging(logname, logmode, theme)`. This creates a default setup where logs are written to file logname in mode logmode. Default is "log.txt" and "a" (for append to file). This replaces the call to [logging.basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig) and works similarly.   
Colors are set by the theme. The theme variable can either be set to a local file or to a url. Examples of themes are available in the [themes](https://github.com/JulienBrn/BeautifulLogger/tree/main/themes) folder. Note that you cannot use the github url directly to load them and should use the rawgithub url instead. For example: [https://cdn.githubraw.com/JulienBrn/BeautifulLogger/main/themes/pycharm.json](https://cdn.githubraw.com/JulienBrn/BeautifulLogger/main/themes/pycharm.json).  
To create your own colors, you should be aware that colors and attributes are then fed to [termcolor](https://pypi.org/project/termcolor/), but not all configurations are supported by all terminals. To view what is supported in your terminal and how it is displayed, you may use the [testcolors script](https://github.com/JulienBrn/BeautifulLogger/blob/main/tests/testcolors.py).
4. `logger = logging.getLogger(__name__)`. This creates a logger with name "__main__" (the relevance of this will be seen latter).
5. Setup the messages you wish to see with `logger.setLevel(logging.INFO)` (for example). See [setLevel](https://docs.python.org/3/library/logging.html#logging.Logger.setLevel) for more information
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

### Changing colors and adding logging levels

Documentation to come. Relevant functions are `beautifullogger.setColor` and `beautifullogger.addLevel`.

### Modifying loggers from imported files/modules

Documentation to come. Does not depend on *BeautifulLogger*  and a basic principle is shown in [complex_usage.py](https://github.com/JulienBrn/BeautifulLogger/blob/main/Examples/complex_usage.py)
