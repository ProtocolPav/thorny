import asyncpg
from datetime import datetime, timedelta


class Pool:
    _pool: asyncpg.Pool

    def __init__(self):
        self._pool: asyncpg.Pool

    def assign(self, connection):
        self._pool = connection

    async def acquire_connection(self):
        print("[SERVER] Acquired connection from Pool at", datetime.now())
        return await self._pool.acquire()


pool = Pool()

