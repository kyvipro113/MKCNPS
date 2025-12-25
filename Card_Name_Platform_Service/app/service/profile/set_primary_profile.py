from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Profile_Info_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *

async def set_primary_profile(payload: PayloadEndUserModel, profile_id: str, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:

        query_reset = {
            "uid": payload.uid,
            "primary_profile": True
        }
        update_reset = {
            "primary_profile": False
        }

        await mongo.update_many(profile_info.__name__, query_reset, update_reset)

        query_set = {
            "_id": ObjectId(profile_id),
            "uid": payload.uid
        }
        update_set = {
            "primary_profile": True
        }

        update = await mongo.update_many(profile_info.__name__, query_set, update_set)
        if update == 0:
            return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.not_found).model_dump(mode="json"), status_code=499)

        return JSONResponse(content=ErrorMessageModel(message=SetPrimaryProfileMsg.set_primary_successful).model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in set_primary_profile - : {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=SetPrimaryProfileMsg.set_primary_failed).model_dump(mode="json"), status_code=400)