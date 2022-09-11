from pydantic import BaseModel


class Input(BaseModel):
    site_name: str
    url: str
    document: str
    label: str

class Response(BaseModel):
    name: str
    document: str
    label: str