from deta import Base
import logging
from urllib.parse import urlparse
from jsonformatter import JsonFormatter

format = '''{
    "level":           "levelname",
    "logger_name":     "%(name)s.%(funcName)s",
    "timestamp":       "asctime",
    "message":         "message"
}'''

def get_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = JsonFormatter(format)

    logHandler = logging.StreamHandler()
    logHandler.setFormatter(formatter)
    logHandler.setLevel(level)

    logger.addHandler(logHandler)
    return logger

def fetch_web_article_data(db: Base, url: str):
    item = db.get(url)
    return item

def fetch_website_data(db: Base, url: str):
    domain = urlparse(url).netloc
    item = db.get(domain)
    return item