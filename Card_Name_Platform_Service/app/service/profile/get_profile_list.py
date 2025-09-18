from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.Error_Msg import *


async def get_profile_list(uid: str, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    profile_list = []
    try:
        pipeline = [
            {"$match": {"uid": uid}} 
        ]
        profile_list = await mongo.aggregate("profile_info", pipeline)
        print(profile_list)
    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in get_profile_list: {str(e)}")
        
