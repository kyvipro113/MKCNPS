from motor.motor_asyncio import AsyncIOMotorClient
from typing import Union
from bson import ObjectId
from Card_Name_Platform_Service.asyn_mongo.collection import *

class MongoDBConfig:
    URI: str
    DB_NAME: str 

class AsyncMongoDB:
    def __init__(self, uri: str=None, db_name: str=None):
        self.client = AsyncIOMotorClient(uri) if uri else AsyncIOMotorClient(MongoDBConfig.URI)
        self.db = self.client[db_name] if db_name else self.client[MongoDBConfig.DB_NAME]

    async def get_collection(self, collection_name: str):
        return self.db[collection_name]
    
    async def find_all(self, collection_name: str, query: dict = {}):
        cursor = self.db[collection_name].find(query)
        documents = []
        async for document in cursor:
            documents.append(document)
        return documents

    async def find_one_id(self, collection_name: str, id: str, **kwargs):
        doc = await self.db[collection_name].find_one({"_id": ObjectId(id)}, kwargs)
        return doc
    
    async def find_one(self, collection_name: str, query: dict, **kwargs):
        doc = await self.db[collection_name].find_one(query, kwargs)
        return doc
    
    async def insert_one(self, collection_name: str, document: dict):
        result = await self.db[collection_name].insert_one(document)
        return str(result.inserted_id)

    async def insert_one_with_id(self, collection_name: str, document: dict, id: str):
        document["_id"] = ObjectId(id)
        result = await self.db[collection_name].insert_one(document)
        return str(result.inserted_id)
    
    async def update_one(self, collection_name: str, id: str, update_fields: dict):
        result = await self.db[collection_name].update_one(
            {"_id": ObjectId(id)},
            {"$set": update_fields}
        )
        return result.modified_count
    
    async def delete_one(self, collection_name: str, id: str):
        result = await self.db[collection_name].delete_one({"_id": ObjectId(id)})
        return result.deleted_count
    
    async def aggregate(self, collection_name: str, pipeline: list):
        cursor = self.db[collection_name].aggregate(pipeline)
        # results = []
        # async for document in cursor:
        #     results.append(document)

        results = await cursor.to_list(length=None)
        return results
    
def load_settings_mongo(MONGO_HOST: str, MONGO_PORT: Union[str, int], USERNAME: Union[str, None], PASSWORD: Union[str, None], db_name):
    MONGO_PORT = str(MONGO_PORT)
    MongoDBConfig.URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}" if not USERNAME and not PASSWORD else f"mongodb://{USERNAME}:{PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
    MongoDBConfig.DB_NAME = db_name

# async def main():
#     load_settings_mongo("localhost", "27017", None, None, "mkcnp")
#     mongo = AsyncMongoDB()
#     # collection_name = "account_info"
#     # # Insert a document
#     # doc = {
#     #     "email": "marinkqh@gmail.com",
#     #     "pwd": "54047024fd89c7c3bc9b9131bf9a76437755925314d6a64d60e629df0882edaa",
#     #     "phone_number": "113",
#     #     "username_link": "nvm169",
#     #     "language": "vietnamese",
#     #     "status": "00",
#     #     "act_login_by_phone_number": False,
#     #     "first_login": False
#     # }
#     # oid_acc_if =  await mongo.insert_one(collection_name=collection_name, document=doc)
#     # print(f"Inserted document ID: {oid_acc_if}")

#     import os
#     import struct
#     import threading
#     import time
#     from datetime import datetime, timezone

#     class ObjectIdGenerator:
#         """
#         Tạo ObjectId theo cấu trúc:
#         [4B timestamp seconds][5B random per-process][3B counter]
#         - timestamp: big-endian
#         - counter: 24-bit, quay vòng
#         Cấu trúc này tương thích định dạng với MongoDB drivers hiện đại.
#         """
#         _lock = threading.Lock()
#         _rand5 = os.urandom(5)                 # 5 byte ngẫu nhiên cố định cho mỗi process
#         _counter = int.from_bytes(os.urandom(3), "big")  # 24-bit counter khởi tạo ngẫu nhiên

#         @classmethod
#         def generate_bytes(cls) -> bytes:
#             ts = int(time.time())
#             with cls._lock:
#                 cls._counter = (cls._counter + 1) & 0xFFFFFF  # giữ 24-bit
#                 counter_bytes = cls._counter.to_bytes(3, "big")

#             ts_bytes = struct.pack(">I", ts)  # 4 byte big-endian
#             return ts_bytes + cls._rand5 + counter_bytes

#         @classmethod
#         def generate(cls) -> str:
#             """Trả về 24 ký tự hex (chuỗi) giống Mongo ObjectId."""
#             return cls.generate_bytes().hex()

#     def decode_oid_hex(oid_hex: str):
#         """
#         Giải mã OID hex (24 hex) -> dict: timestamp, random5, counter
#         """
#         b = bytes.fromhex(oid_hex)
#         if len(b) != 12:
#             raise ValueError("ObjectId phải dài 12 byte (24 hex).")
#         ts = struct.unpack(">I", b[0:4])[0]
#         rand5 = b[4:9]
#         counter = int.from_bytes(b[9:12], "big")
#         return {
#             "timestamp": ts,
#             "datetime_utc": datetime.fromtimestamp(ts, tz=timezone.utc),
#             "random5_hex": rand5.hex(),
#             "counter": counter,
#         }


#     from pydantic import BaseModel, model_validator
#     from typing import List, Dict, Any, Optional, Union
#     from bson import ObjectId    

#     class card_info(BaseModel):
#         _id: Union[str, ObjectId] = ""
#         card_id_old: str = ""
#         uid: str = ""
#         status: str = "01"
#         pin: str = ""

#     collection_name = "card_info"

#     oid = ObjectId(ObjectIdGenerator.generate())
#     card_if = card_info(
#         _id=oid,
#         card_id_old="a3f005c4fb6e",
#         uid="68b1241c91b161bf70c9cf35",
#         status="00",
#         pin="617a72"
#     )

#     oid_card_if =  await mongo.insert_one_with_id(collection_name=collection_name, document=card_if.model_dump(mode="python"), id=str(oid))
#     print(f"Inserted document ID: {oid_card_if}")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())