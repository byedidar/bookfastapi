from datetime import date
from fastapi import Query
from pydantic import BaseModel

class SBook(BaseModel):
    id: int
    name: str
    author: str
    date_of_book: date
    checked: bool = False