from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id:                 int
    username:           str
    age:                int|None = None
    gender:             str|None = None
    bio:                str|None = None
    # registration_date:  datetime

    class Config:
        orm_mode = True