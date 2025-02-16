from pydantic import BaseModel

class URLSchema(BaseModel):
    value: str

class UserSchema(BaseModel):
    username: str
    password: str
