import asyncio
from redis.asyncio import BlockingConnectionPool, Redis

class Redis_Client(object):
    HOST: str
    PORT: str

    def __init__(self, expiry_time=600, db=0):
        try:
            self.__pool = BlockingConnectionPool(host=Redis_Client.HOST, port=Redis_Client.PORT, db=db)
            self.expiry_time=expiry_time
        except Exception as e:
            raise ValueError(e)

    def __await__(self):
        return self.init().__await__()
    
    async def init(self):
        self._pool = await Redis(connection_pool=self.__pool)
        return self
    
    async def set(self, key, value):
        # await self._pool.set(key, value)
        await self._pool.set(key, value)
        await self._pool.expire(key, self.expiry_time)

    async def get(self, key):
        return await self._pool.get(key)
    
    async def delete(self, key):
        await self._pool.delete(key)
    

def load_settings_redis(REDIS_HOST: str, REDIS_PORT: str):
    Redis_Client.HOST = REDIS_HOST
    Redis_Client.PORT = REDIS_PORT
    # print(Redis_Client.HOST)
    # print(Redis_Client.PORT)
