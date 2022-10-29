from deta import Base
import logging
from urllib.parse import urlparse
from jsonformatter import JsonFormatter
from newspaper import Article

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

def extract_heuristics(url: str):
    article_report = {
        'authors': None,
        'published_date': None
    }
    article = Article(url, language='es')
    article.download()
    try:
        article.parse()
    except:
        return article_report
    
    article_report['authors'] = article.authors
    article_report['published_date'] = article.publish_date.strftime('%d/%m/%Y')
    return article_report

def fetch_web_article_data(db: Base, url: str):
    item = db.get(url)
    if 'https' in url and item is None:
        url = url.replace("https", "http")
        item = db.get(url)
    if item is None:
        item = {'category': None}
    return item

def fetch_website_data(db: Base, url: str):
    domain = urlparse(url).netloc
    item = db.get(domain)
    if item is None:
        item = {'count': None}
    return item
