from app.database import Base
from sqlalchemy import Column, Integer, String, Computed, Date, Boolean

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    date_of_book = Column(Date, nullable=False)
    checked = Column(Boolean, nullable=False)


