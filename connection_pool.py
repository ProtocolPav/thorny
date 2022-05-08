import asyncpg
from datetime import datetime, timedelta
import json
import asyncio


class Pool:
    pool: asyncpg.Pool

    def __init__(self):
        self.pool: asyncpg.Pool

    async def create_pool(self):
        config = json.load(open('../thorny_data/config.json', 'r+'))
        pool_object = await asyncpg.create_pool(database=config['database']['name'],
                                                user=config['database']['user'],
                                                password=config['database']['password'],
                                                max_inactive_connection_lifetime=10.0,
                                                max_size=300)
        print("[SERVER] Successfully pooled Database at", datetime.now())
        self.pool = pool_object

    async def acquire_connection(self):
        connection = await self.pool.acquire(timeout=10.0)
        print("[SERVER] Acquired connection from Pool at", datetime.now())
        print(f"[SERVER] {self.pool.get_idle_size()} idle connections, {self.pool.get_size()} total connections")
        return connection

    async def release(self, conn: asyncpg.Connection):
        await self.pool.release(conn)
        print("[SERVER] Released connection to pool at", datetime.now())

    async def test_query(self):
        async with self.pool.acquire() as connection:
            abc = await connection.fetch("""SELECT * FROM thorny.user""")
            print(f"[SERVER] {self.pool.get_idle_size()} idle connections, {self.pool.get_size()} total connections")
            print(abc)
        print(f"[SERVER] {self.pool.get_idle_size()} idle connections, {self.pool.get_size()} total connections")


pool = Pool()
asyncio.get_event_loop().run_until_complete(pool.create_pool())
