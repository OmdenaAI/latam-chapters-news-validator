from pydantic import BaseModel

#
# Models for reporting requests
#

class ReportInput(BaseModel):
    site_name: str
    url: str
    document: str
    label: str

class ReportResponse(BaseModel):
    name: str
    document: str
    label: str

#
# Models for contextualization requests
#

class ContextInput(BaseModel):
    url: str

class ContextResponse(BaseModel):
    label: str = None
    website_count: int = None
    authors: list = None
    published_date: str = None