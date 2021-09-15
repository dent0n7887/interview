from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from utils.AppMiddleware import HandleError


class AtomicTransaction():
    """
    Аналог transaction.atomic из Django
    Транзакции, указанные внутри контекста необходимо оборачивать в блок try
    В блок except обязательно прописывать session.rollback()
    Также вы можете реализовать повторение транзакции (указать количество повторений - параметр attempt),
    если сталкиваетесь с кейсами блокировки таблиц
    """
    def __init__(self, session_generator: Type[AsyncSession], attempts: int = 0):
        self._session_generator = session_generator
        self._session = None
        self._attempts = attempts

    async def __aenter__(self):
        self._session = self._session_generator()

        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        for attempt in range(self._attempts + 1):
            try:
                await self._session.commit()
                break
            except:
                if attempt == self._attempts:
                    raise HandleError('Transaction Failed')
                continue

