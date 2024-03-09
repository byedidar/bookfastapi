from fastapi import FastAPI, Query,Depends
from datetime import date
from typing import Optional
from pydantic import BaseModel

# from app.bookings.router import router as bookings_router
# from app.users.router import router as users_router
from app.book_task.router import router as book_router



app = FastAPI(
    title = "First App"
)

app.include_router(book_router)
# app.include_router(users_router)
# app.include_router(bookings_router)





