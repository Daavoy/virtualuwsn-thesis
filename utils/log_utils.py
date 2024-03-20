import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
import os

def getTimedRotatingFileHandler(name, logfile):
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s]:%(message)s', datefmt="%H:%M:%S")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(logfile, when="m", interval=30, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def getFileHandler(name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    log_filename = f"{name}.{timestamp}.log"
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s]:%(message)s', datefmt="%H:%M:%S")
    logger = logging.getLogger(log_filename)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_filename)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def delete_all_logs(logpath):
    if not os.path.exists(logpath):
        print(f"Error: Folder '{logpath}' does not exist.")
        return
    
    logs = [f for f in os.listdir(logpath) ]
    for log in logs:
        os.remove(os.path.join(logpath, log))

def delete_logs_before_timestamp(logpath, timestamp):
    if not os.path.exists(logpath):
        print(f"Error: Folder '{logpath}' does not exist.")
        return

    logs = [f for f in os.listdir(logpath)]
    deleted = 0
    
    for log in logs:
        log_path = os.path.join(logpath, log)
        try:
            log_timestamp_str = log.split('.')[1]
            log_timestamp = datetime.strptime(log_timestamp_str, "%Y%m%d_%H%M%S")

            if log_timestamp < timestamp:
                os.remove(log_path)
                deleted += 1

        except Exception as e:
            print(f"Error processing log file {log_path}: {e}")

    if deleted > 0:
        print(f"Deleted {deleted} log files")

def delete_logs_older_than_days(logpath, days):
    timestamp = datetime.now() - timedelta(days=days)
    delete_logs_before_timestamp(logpath, timestamp)