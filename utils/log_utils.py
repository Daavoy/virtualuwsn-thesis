import logging
from logging.handlers import TimedRotatingFileHandler

def getTimedRotatingFileHandler(name, logfile):
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s]:%(message)s', datefmt="%H:%M:%S")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(logfile, when="m", interval=30, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger