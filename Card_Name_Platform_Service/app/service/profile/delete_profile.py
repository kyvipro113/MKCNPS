from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.model.Profile_Info_Model import *

async def delete_profile(payload: PayloadEndUserModel, profile_id: str, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(payload.uid),
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "change_profile": 1,
                    "account_mode": 1,
                }
            }
        ]

        data = await mongo.aggregate(account_info.__name__, pipeline)
        print(data)
        if data is None:
            return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.not_found).model_dump(mode="json"), status_code=499)
        
        account_if = ProfileInfoModelRtn(**data[0])
        print(f"Profile to delete: {account_if}")
        if account_if.change_profile is False:
            return JSONResponse(content=ErrorMessageModel(message=DeleteProfileMsg.no_permission).model_dump(mode="json"), status_code=498)

        pipeline_profile = [
            {
                "$match": {
                    "_id": ObjectId(profile_id),
                    "uid": payload.uid
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "primary_profile": 1,
                }
            }
        ]
        data_profile = await mongo.aggregate(profile_info.__name__, pipeline_profile)
        print(data_profile)
        if data_profile is None:
            return JSONResponse(content=ErrorMessageModel(message=ProfileMsg.not_found).model_dump(mode="json"), status_code=497)
        
        profile_if = ProfileInfoModelRtn(**data_profile[0])
        if profile_if.primary_profile is True:
            return JSONResponse(content=ErrorMessageModel(message=DeleteProfileMsg.cannot_delete_primary).model_dump(mode="json"), status_code=496)
        
        await mongo.delete_one(profile_info.__name__, profile_id)

        return JSONResponse(content=ErrorMessageModel(message=DeleteProfileMsg.delete_profile_successful).model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in delete_profile - : {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=DeleteProfileMsg.delete_profile_failed).model_dump(mode="json"), status_code=500)
