import logging
from fastapi import FastAPI, HTTPException
from deta import Base
from models import (
    ReportInput,
    ReportResponse,
    ContextInput,
    ContextResponse
)
from datetime import datetime
from utils import fetch_web_article_data, fetch_website_data
from utils import get_logger

logger = get_logger(__name__)
app = FastAPI()

#
# get connection to all DBs
#

# DB of web URLs that users report as fake 
reported_news_db = Base("reported-news-db")

# DB of scraped news articles found in fact checkers or annotated datasets
web_article_db = Base("web-article-db")

# DB of statistics for each web site
website_db = Base("website-db")

#
# Endpoints
#

@app.get("/health")
def health_check():
    """
    Regular Health endpoint
    """
    return {"health":True}

@app.post("/report", response_model=ReportResponse)
def upload_document(item: ReportInput):
    """
    Endpoint used to save reported web article info into DB
    """
    logger.info(f"Creating new row in reported-news-db DB")
    timestamp = datetime.utcnow().strftime('%Y-%m-%d.%H:%M:%S')
    doc = reported_news_db.put(
        data = {
            "name": item.site_name,
            "document": item.document,
            "label": item.label,
            "save_date": timestamp
        },
        key = item.url
    )

    return doc

@app.post("/contextualize", response_model=ContextResponse)
def contextualize(item: ContextInput):
    """
    Endpoint used to contextualize web news article
    """
    logger.info(f"Processing contextualize request for URL: {item.url}")
    report = {}

    # Check if article has been reported as non-trustful
    try:
        web_article_item = fetch_web_article_data(db=web_article_db, url=item.url)
        if web_article_item is not None:
            report['label'] = web_article_item['category']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    # Check if website has articles reported as non-trustful
    try:
        website_item = fetch_website_data(db=website_db, url=item.url)
        if website_item is not None:
            report['website_count'] = website_item['count']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    # TODO: Get article extracted info (author, date, etc)
    
    return report
