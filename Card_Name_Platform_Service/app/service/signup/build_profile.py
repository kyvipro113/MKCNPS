from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *

async def build_profile(uid: str, profile: profile_info, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name="build_profile", name_logger="build_profile", file_mode="a")
    
