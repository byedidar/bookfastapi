from app.book_task.models import Book
from app.dao.base import BaseDAO

class BookDAO(BaseDAO):
    model = Book