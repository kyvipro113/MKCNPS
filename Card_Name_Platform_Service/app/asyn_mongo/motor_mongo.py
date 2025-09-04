from motor.motor_asyncio import AsyncIOMotorClient
from typing import Union
from bson import ObjectId

class MongoDBConfig:
    URI: str
    DB_NAME: str 

class AsyncMongoDB:
    def __init__(self, uri: Union[str, None], db_name: Union[str, None]):
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

    async def find_one_id(self, collection_name: str, id: str):
        doc = await self.db[collection_name].find_one({"_id": ObjectId(id)})
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
    
def load_settings_mongo(MONGO_HOST: str, MONGO_PORT: str, USERNAME: Union[str, None], PASSWORD: Union[str, None], db_name):
    MongoDBConfig.URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}" if not USERNAME and not PASSWORD else f"mongodb://{USERNAME}:{PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
    MongoDBConfig.DB_NAME = db_name