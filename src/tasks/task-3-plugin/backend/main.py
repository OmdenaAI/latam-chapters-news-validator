from fastapi import FastAPI
from deta import Base
from fastapi.responses import JSONResponse
from models import Input, Response
import os

app = FastAPI()
db = Base("news-db")

@app.get("/health")
def health_check():
    return {"health":True}

@app.post("/upload", response_model=Response)
def upload_document(item: Input):
    doc = db.put(
        data = {
            "name": item.site_name,
            "document": item.document,
            "label": item.label
        },
        key = item.url
    )

    return doc
