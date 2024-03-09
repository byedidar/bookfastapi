from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.book_task.dao import BookDAO
from app.book_task.schemas import SBook
from datetime import date


router = APIRouter(
    prefix="/v1/book",
    tags=["Book"],
)

class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    date_of_book: Optional[date] = None
    checked: Optional[bool] = None


class BookReplace(BaseModel):
    name: str
    author: str
    date_of_book: date
    checked: bool = False


@router.post("")
async def register_book(book_data: SBook):
    await BookDAO.add(id=int(book_data.id), name=book_data.name, author=book_data.author, date_of_book=book_data.date_of_book, checked=book_data.checked)


@router.get("{id}/")
async def get_book(id):
    return await BookDAO.find_by_id(int(id))

@router.patch("/{id}")
async def update_item(id: int, book_update: BookUpdate):
    update_data = book_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")
    updated_book = await BookDAO.change(data=update_data, id=id)
    if not updated_book:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
    
    return updated_book



@router.put("/{book_id}") 
async def replace_book(book_id: int, book_data: BookReplace) -> SBook:
    new_data = book_data.dict(exclude_unset=True)   
    replaced_or_new_book = await BookDAO.replace(model_id=book_id, new_data=new_data)
    if replaced_or_new_book is None:
        raise HTTPException(status_code=404, detail="Book not found and failed to create a new one.")

    return replaced_or_new_book


@router.delete("{id}")
async def delete_book(id: int):
    await BookDAO.delete(int(id))
    return {"message": f"Book with id {id} was succesfully deleted"}
   