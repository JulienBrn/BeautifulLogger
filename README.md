# BeautifulLogger
A beautiful default configuration for Python loggers. Used as an example of why loggers may be useful.

My goal is to motivate you to use loggers instead of prints using the logging module. The benefits of using loggers instead of prints for someone who masters loggers is:

- Being able to save all prints/logs to file easily
- Provide different "levels" of print messages (warning, error, critical, debug, info...)
- Automatically add information to prints (no additional code per print required) time, file, line, stack-trace, ...
- Format print/log message using colors, ...
- Filter prints/logs depending on what one wants. For example all messages when debugging and only warnings and errors when running.

I will not attempt to do a full tutorial or make you a master of the logging module. However, I will discuss 3 different use patterns :

1. You work in only 1 python file and you do not have much time to spend understanding loggers but want to see some the benefits (benefits can then be added without changing existing code).  Simply do the following :
  - Add the following lines at the beginning of your file
```
        import logging

        logging.basicConfig(level=0, filename="log.txt", filemode="a", format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s @ %(filename)s:%(lineno)s')
        logging.info("New Run Start")
        logger = logging.getLogger(__name__)
        logger_handler = logging.StreamHandler()
        logger.addHandler(logger_handler)
        import beautifullogger #Module I created for nice formatting
        beautifullogger.make_beautiful(logger_handler) #Optional, used for nicer formatting
        logger_handler.setLevel(logging.DEBUG) #Or logging.WARNING, logging.ERROR, ...
        Use one of the following commands instead of print("msg")
            logger.debug("msg")
            logger.info("msg")
            logger.warning("msg")
            logger.error("msg")
            logger.critical("msg")
``` 
   - You are all set. The benefits are medium, but your code is ready for other benefits ! An example is given [here](https://github.com/JulienBrn/BeautifulLogger/blob/main/Examples/simple_usage.py).
2. You are interested in how logging works. Look [this](https://github.com/JulienBrn/BeautifulLogger/blob/main/tests/test_beautifullogger.py) example and read the comments.
3. You work with multiple files and might create your own modules for others and perhaps even upload them to Pypi. Or you are simply curious. Please read a full tutorial or write me an email.
