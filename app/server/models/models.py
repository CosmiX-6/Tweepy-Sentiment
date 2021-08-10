from typing import Optional
from pydantic import BaseModel, Field

class SearchSchema(BaseModel):
    search_txt : str = Field(...)

    class Config:
        schema_extra = {
            "emaxple": {
                "search" : "Jeff Bezos"
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}