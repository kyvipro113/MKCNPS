from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.model.Profile_List_Model import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *


async def get_profile_list_user(payload: PayloadEndUserModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    profile_list = []
    try:
        pipeline = [
            {"$match": {"uid": payload.uid}},
            {
                "$project": {
                    "_id": 1,
                    "name": 1,
                    "designation": 1,
                    "avatar_location": 1,
                    "primary_profile": 1
                }
            }
        ]
        profile_list = await mongo.aggregate(profile_info.__name__, pipeline)
        if len(profile_list) == 0:
            return JSONResponse(content=ProfileListModel(message=ProfileMsg.profile_list_empty).model_dump(mode="json"), status_code=499)
        short_profiles = [ShortProfileModel(**profile) for profile in profile_list]
        for sprofile in short_profiles:
            sprofile.id = str(sprofile.id)
            if sprofile.avatar_location != "":
                folder_file_avt = sprofile.avatar_location.split('/')
                sprofile.avatar_location = await Minio_Client.get_url(bucket_name=folder_file_avt[0], object_name=folder_file_avt[1])
                #sprofile.avatar_location = await Minio_Client.get_url_no_presign(bucket_name=folder_file_avt[0], object_name=folder_file_avt[1])
        profile_list_model = ProfileListModel(short_profiles=short_profiles, message=ProfileMsg.get_list_profile_successful)
        return JSONResponse(content=profile_list_model.model_dump(mode="json"), status_code=200)
    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in get_profile_list: {str(e)}")
        return JSONResponse(content=ProfileListModel(message=ProfileMsg.get_list_profile_failed).model_dump(mode="json"), status_code=400)
        
