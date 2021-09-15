from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession


class HandleSession:
    """
    Если вместо создания новой сессии была передана уже существующая сессия - то в конце она не коммитится
    Если сессия не была передана - то по умолчанию в конце она закоммитится.
    Если вы по какой-то причине не хотите коммитить по умолчанию сессию - установите аргумент need_commit в значение False
    """
    def __init__(self, session_generator: Type[AsyncSession], session=None):
        self._session_generator = session_generator
        self._session = session

    async def __aenter__(self):
        if self._session:
            setattr(self._session, 'need_commit', False)
        else:
            self._session = self._session_generator()
            setattr(self._session, 'need_commit', True)

        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session.need_commit:
            await self._session.commit()

