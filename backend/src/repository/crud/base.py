from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession


class BaseCRUDRepository:
    def __init__(self, async_session: SQLAlchemyAsyncSession):
        self.session = async_session
