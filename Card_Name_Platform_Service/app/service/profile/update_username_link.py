from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Token_Model import *

async def update_username_link(payload: PayloadEndUserModel, new_username_link: str, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        query = {
            "_id": {"$ne": ObjectId(payload.uid)},
            "username_link": new_username_link
        }

        existed = await mongo.find_one(account_info.__name__, query)
        if existed:
            return JSONResponse(content=ErrorMessageModel(message=UsernameLinkMsg.already_exists).model_dump(mode="json"), status_code=499)
        
        update = {
            "username_link": new_username_link
        }
        await mongo.update_one(account_info.__name__, payload.uid, update)
        return JSONResponse(content=ErrorMessageModel(message=UsernameLinkMsg.update_successful).model_dump(mode="json"), status_code=200)
    
    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in update_username_link: {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=UsernameLinkMsg.update_failed).model_dump(mode="json"), status_code=500)