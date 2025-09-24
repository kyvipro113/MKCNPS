import asyncio
from redis.asyncio import BlockingConnectionPool, Redis, ConnectionPool
from typing import Union
import json

# class RedisClient(object):
#     HOST: str
#     PORT: str

#     def __init__(self, expiry_time=600, db=0):
#         try:
#             self.__pool = BlockingConnectionPool(host=RedisClient.HOST, port=RedisClient.PORT, db=db)
#             self.expiry_time=expiry_time
#         except Exception as e:
#             raise ValueError(e)

#     def __await__(self):
#         return self.init().__await__()
    
#     async def init(self):
#         self._pool = await Redis(connection_pool=self.__pool)
#         return self
    
#     async def set(self, key, value):
#         # await self._pool.set(key, value)
#         await self._pool.set(key, value)
#         await self._pool.expire(key, self.expiry_time)

#     async def get(self, key):
#         return await self._pool.get(key)
    
#     async def delete(self, key):
#         await self._pool.delete(key)

class RedisClient(object):
    HOST: str
    PORT: str

    def __init__(self, db=0, expiry_time=600, decode_res=True):
        self.expiry_time = expiry_time
        self.decode_res = decode_res
        self.__pool  = ConnectionPool(
            host=RedisClient.HOST,
            port=RedisClient.PORT,
            db=db,
            decode_responses=decode_res
        )
        # self._client = Redis(connection_pool=self.__pool)
        ## Use context manager for each operation


    async def set(self, key, value, ex=-1):
        async with Redis(connection_pool=self.__pool) as client:
            if ex == -1:
                await client.set(key, value=value, ex=self.expiry_time)
            else:
                await client.set(key, value=value, ex=ex)


    async def set_json(self, key, value: dict, ex=-1):
        value_str = json.dumps(value)
        async with Redis(connection_pool=self.__pool) as client:
            if ex == -1:
                await client.set(key, value=value_str, ex=self.expiry_time)
            else:
                await client.set(key, value=value_str, ex=ex)

    async def get(self, key)->Union[str, bytes]:
        async with Redis(connection_pool=self.__pool) as client:
            return await client.get(key)    


    async def get_json(self, key)->Union[dict, None]:
        async with Redis(connection_pool=self.__pool) as client:
            value_str = await client.get(key)
            if value_str is not None:
                if self.decode_res:
                    return json.loads(value_str)
                else:
                    return json.loads(value_str.decode('utf-8'))
            return None

    async def pop(self, key)->Union[str, bytes]:
        async with Redis(connection_pool=self.__pool) as client:
            value = await client.get(key)
            if value is not None:
                await client.delete(key)
            return value

    async def pop_json(self, key)->Union[dict, None]:
        async with Redis(connection_pool=self.__pool) as client:
            value_str = await client.get(key)
            if value_str is not None:
                await client.delete(key)
                if self.decode_res:
                    return json.loads(value_str)
                else:
                    return json.loads(value_str.decode('utf-8'))
            return None

    async def delete(self, key):
        async with Redis(connection_pool=self.__pool) as client:
            await client.delete(key)

    
    async def exists(self, key)->bool:
        async with Redis(connection_pool=self.__pool) as client:
            return await client.exists(key) > 0
        
    async def assert_value(self, key, expected_value, is_pop=True)->bool:
        print(f"Key: {key}")
        async with Redis(connection_pool=self.__pool) as client:
            value = None
            if is_pop:
                value = await self.pop(key)
            else:
                value = await client.get(key)
            print(f"Assert value: {value}, expected: {expected_value}")
            if value is None:
                return False
            return value == expected_value


def load_settings_redis(REDIS_HOST: str, REDIS_PORT: str):
    RedisClient.HOST = REDIS_HOST
    RedisClient.PORT = REDIS_PORT
    # print(RedisClient.HOST)
    # print(RedisClient.PORT)
