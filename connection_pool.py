import asyncpg
from datetime import datetime, timedelta
import json
import asyncio


async def create_pool(loop=None):
    # config = json.load(open('../thorny_data/config.json', 'r+'))
    # pool_object = await asyncpg.create_pool(database=config['database']['name'],
    #                                         user=config['database']['user'],
    #                                         password=config['database']['password'],
    #                                         max_inactive_connection_lifetime=10.0,
    #                                         max_size=300,
    #                                         loop=loop)
    pool_object = await asyncpg.create_pool(database="thorny",
                                            user="thorny",
                                            password="postgrespw",
                                            host="postgres",
                                            port=5432,
                                            max_inactive_connection_lifetime=10.0,
                                            max_size=300,
                                            loop=loop
                                            )
    return pool_object

pool = asyncio.get_event_loop().run_until_complete(create_pool())
# asyncio.run(pool.create_pool())
