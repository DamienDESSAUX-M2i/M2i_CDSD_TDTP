# Logging package

## Import

```python
import logging
```

## Logs levels

```python
logging.debug() # Provides detailed information that’s valuable to you as a developer.
logging.info() # Provides general information about what’s going on with your program.
logging.warning() # Indicates that there’s something you should look into.
logging.error() # Alerts you to an unexpected problem that’s occurred in your program.
logging.critical() # Tells you that a serious error has occurred and may have crashed your app.
```

Notice that the debug() and info() messages didn’t get logged. This is because, by default, the logging module logs the messages with a severity level of WARNING or above. You can change that by configuring the logging module to log events of all levels. 

```python
logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
# WARNING:root:This is a warning message
logging.error("This is an error message")
# ERROR:root:This is an error message
logging.critical("This is a critical message")
# CRITICAL:root:This is a critical message
```

## Adjusting the Log Level

```python
logging.basicConfig(level=logging.DEBUG)
logging.debug("This will get logged.")
# DEBUG:root:This will get logged.
```

## Formatting the Output

```python
logging.basicConfig(
    format="{asctime} - {levelname} - {name} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
logging.error("Something went wrong!")
# 2025-11-12 08:37 - ERROR - root - Something went wrong!
```

## Logging to a File

```python
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="at",
    format="{asctime} - {levelname} - {name} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
logging.warning("Save me!")
# Inside app.log
# 2025-11-12 08:40 - WARNING - root - Save me!
```

## Displaying Variable Data

```python
logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)
name = "Damien"
logging.debug(f"name : {name}")
# 2025-07-22 14:49 - DEBUG - name : 'Damien'
```

## Capturing Stack Traces

```python
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
donuts = 5
guests = 0
try:
    donuts_per_guest = donuts / guests
except ZeroDivisionError:
    logging.error("DonutCalculationError", exc_info=True)
# Inside app.log
# Traceback (most recent call last):
#   File "c:\Users\Administrateur\Documents\python_logger\main.py", line 13, in <module>
#     donuts_per_guest = donuts / guests
#                        ~~~~~~~^~~~~~~~
# ZeroDivisionError: division by zero
```

Calling logging.exception() is like calling logging.error(exc_info=True). Since the logging.exception() function always dumps exception information, you should only call logging.exception() from an exception handler.

When you use logging.exception(), it shows a log at the level of ERROR. If you don’t want that, you can call any of the other logging functions from debug() to critical() and pass the exc_info parameter as True.

```python
try:
    donuts_per_guest = donuts / guests
except ZeroDivisionError:
    logging.exception("DonutCalculationError")
```

## Creating a Custom Logger

```python
logger = logging.getLogger(__name__)
logger.warning("Look at my logger!")
# Look at my logger!
```

## Using Handlers

The StreamHandler class will send your logs to the console. The FileHandler class writes your log records to a file. To define where and how you want to write the logs, you provide a file path, an opening mode, and the encoding.

```python
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
```

After you’ve instantiated your handlers, you must add them to the logger. For this, you use the .addHandler() method:

```python
logger.addHandler(console_handler)
logger.addHandler(file_handler)
print(logger.handlers) # Display handlers of the logger.
# <StreamHandler <stderr> (NOTSET)>
# <FileHandler /Users/RealPython/Desktop/app.log (NOTSET)>
logger.warning("Watch out!")
```

## Adding Formatters to Your Handlers


```python
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
logger.addHandler(console_handler)
logger.addHandler(file_handler)
formatter = logging.Formatter(
    "{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
console_handler.setFormatter(formatter)
logger.warning("Stay calm!")
```

## Setting the Log Levels of Custom Loggers

The default log level of your custom logger is 0, which stands for NOTSET. Still, the string representation of your logger shows the WARNING log level. That’s because a custom logger inherits the log level of its parent logger if you haven’t yet set the log level manually.

```python
logger = logging.getLogger(__name__)
print(logger.level) # Display level of a logger
# 0
print(logger)
# <Logger __main__ (WARNING)>
print(logger.parent)
# <RootLogger root (WARNING)>
```

The returned value of .getEffectiveLevel() is an integer that stands for the log level.

```python
logger.getEffectiveLevel()
# 30
```

Numeric Value | Log Level
:-:|:-:
0 | NOTSET
10 | DEBUG
20 | INFO
30 | WARNING
40 | ERROR
50 | CRITICAL

You use the .setLevel() method to set the log level of your logger.

```python
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.setLevel(10) # other way to set level
# logger.setLevel("INFO") # other way to set level
formatter = logging.Formatter("{levelname} - {message}", style="{")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.debug("Just checking in!")
logger.info("Just checking in, again!")
# INFO - Just checking in, again!
```

Since the log level of logger is set to INFO, the console_handler that you added to logger doesn’t show logs that have a log level lower than INFO, ie DEBUG.

```python
print(console_handler)
# <StreamHandler <stderr> (NOTSET)>
console_handler.setLevel("DEBUG")
logger.debug("Just checking in!")
print(console_handler)
# <StreamHandler <stderr> (DEBUG)>
```

With this behavior in mind, it can be helpful during development to set your logger’s log level to DEBUG and let each handler decide their lowest log level

```python
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
formatter = logging.Formatter("{levelname} - {message}", style="{")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
file_handler.setLevel("WARNING")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.debug("Just checking in!")
# DEBUG - Just checking in!
logger.warning("Stay curious!")
# WARNING - Stay curious!
logger.error("Stay put!")
# ERROR - Stay put!
```

## Filtering Logs

The filter you’ll create will make sure the handler that outputs logs into the console only shows DEBUG messages.

```python
def show_only_debug(record):
    return record.levelname == "DEBUG"

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
formatter = logging.Formatter("{levelname} - {message}", style="{")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")
console_handler.setFormatter(formatter)
###
console_handler.addFilter(show_only_debug)
###
logger.addHandler(console_handler)

file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
file_handler.setLevel("WARNING")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.debug("Just checking in!")
# DEBUG - Just checking in!
logger.warning("Stay curious!")
logger.error("Stay put!")
```