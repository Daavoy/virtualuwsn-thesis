import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def getTimedRotatingFileHandler(name, logfile):
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s]:%(message)s', datefmt="%H:%M:%S")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(logfile, when="m", interval=30, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def getFileHandler(name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{name}_{timestamp}.log"
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s]:%(message)s', datefmt="%H:%M:%S")
    logger = logging.getLogger(log_filename)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_filename)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger