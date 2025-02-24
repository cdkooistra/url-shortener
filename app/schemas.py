from pydantic import BaseModel

class URLSchema(BaseModel):
    value: str

# Additional schema for updates as needed for tests
class URLUpdateSchema(BaseModel):
    url: str