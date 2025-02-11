from pydantic import BaseModel

class URLSchema(BaseModel):
    value: str
