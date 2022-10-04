import pandas as pd
from urllib.parse import urlparse
from deta import Deta
from datetime import datetime
import os

deta = Deta(os.environ['PROJECT_KEY'])
web_article_db = deta.Base("web-article-db")
web_site_db = deta.Base("website-db")

def get_url_domain(url: str):
    return urlparse(url).netloc

data_train = pd.read_excel("~/Downloads/train.xlsx")
data_dev = pd.read_excel("~/Downloads/development.xlsx")
data_test = pd.read_excel("~/Downloads/test.xlsx")

data = pd.concat([
    data_train,
    data_dev,
    data_test
]).reset_index()

data =  data[['Category', 'Link', 'Source']]
data = data[~data.Link.isnull()] # remove nulls

data['Domain'] = data['Link'].apply(get_url_domain)
data = data[data['Category'] == 'Fake']

for row in data.to_numpy():
    web_site_db.update(
        updates = {
            "count": 0
        }, 
        key = row[3]
    ) 

for row in data.to_numpy():
    try:
        print(row)
        timestamp = datetime.utcnow().strftime('%Y-%m-%d.%H:%M:%S')
        web_article_result = web_article_db.put(
            data = {
                "url": row[1],
                "domain": row[3],
                "category": row[0],
                "save_date": timestamp
            },
            key = row[1]
        )

        web_site_result = web_site_db.get(key = row[3])
        if web_site_result is None:
            web_site_db.put(
                data = {
                    "domain": row[3],
                    "count": 1,
                    "update_date": timestamp
                },
                key = row[3]
            )
        else:
            web_site_db.put(
                data = {
                    "domain": row[3],
                    "count": web_site_result['count']+1,
                    "update_date": timestamp
                },
                key = row[3]
            )
    except Exception as e:
        print("Error: "+str(e))