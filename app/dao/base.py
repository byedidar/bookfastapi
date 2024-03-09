
from sqlalchemy import delete, insert, select, update
from app.database import async_session_maker

class BaseDAO:
    model = None
    @classmethod
    async def find_by_id(cls, model_id:int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, model_id:int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == model_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def change(cls, data,**filter_by ):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(**filter_by).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()   
        
    
    @classmethod
    async def replace(cls, model_id: int, new_data: dict):
        async with async_session_maker() as session:
            exists_query = select(cls.model).filter_by(id=model_id)
            exists_result = await session.execute(exists_query)
            existing_entity = exists_result.scalar_one_or_none()

            if existing_entity is None:
                query = insert(cls.model).values(id=model_id, **new_data)
                await session.execute(query)
            else:
                query = update(cls.model).filter_by(id=model_id).values(**new_data)
                await session.execute(query)

            await session.commit()
            return await cls.find_by_id(model_id)