from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Account_Info_Model import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *
from Card_Name_Platform_Service.app.model.Token_Model import *

async def get_settings_account(payload: PayloadEndUserModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(payload.uid)
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "phone_number": 1,
                    "email": 1,
                    "act_login_by_phone_number": 1
                }
            }
        ]
        account_data = await mongo.aggregate(account_info.__name__, pipeline)
        print(account_data)
        
        if not account_data:
            return JSONResponse(content=AccountSettingsModel(message=AccountSettingsMsg.not_found).model_dump(mode="json"), status_code=499)

        pipeline = [
            {
                "$match": {
                    "uid": payload.uid,
                    "primary_profile": True
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "avatar_location": 1,
                    "name": 1
                }
            }
        ]

        profile_data = await mongo.aggregate(profile_info.__name__, pipeline)
        print(profile_data)
        profile = profile_data[0] if profile_data else {}
        
        account_settings = AccountSettingsModel(**account_data[0], **profile, message=AccountSettingsMsg.get_account_setting_successful)
        
        if account_settings.avatar_location:
            folder_file_avt = account_settings.avatar_location.split("/")
            account_settings.avatar_location = await Minio_Client.get_url(bucket_name=folder_file_avt[0], object_name=folder_file_avt[1])

        return JSONResponse(content=account_settings.model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception get_setttings_account: {str(e)}")
        return JSONResponse(content=AccountSettingsModel(message=AccountSettingsMsg.get_account_setting_failed).model_dump(mode="json"), status_code=500)



