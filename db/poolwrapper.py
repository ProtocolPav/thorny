import asyncio
import json
import asyncpg as pg

class PoolWrapper:
    __pool: pg.Pool

    async def init_pool(self):
        config = json.load(open('../thorny_data/config.json', 'r+'))
        self.__pool = await pg.create_pool(database=config['database']['name'],
                                         user=config['database']['user'],
                                         password=config['database']['password'],
                                         host=config['database']['host'],
                                         port=5432,
                                         max_inactive_connection_lifetime=10.0,
                                         max_size=300,
                                         loop=None)

    def connection(self):
        return self.__pool.acquire()

pool_wrapper = PoolWrapper()
asyncio.get_event_loop().run_until_complete(pool_wrapper.init_pool())