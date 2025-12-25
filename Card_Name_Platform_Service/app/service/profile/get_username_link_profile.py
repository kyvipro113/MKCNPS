from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import * 
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.model.Profile_Info_Model import *

async def get_username_link_profile(payload, ip: str):
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
                    "username_link": 1
                }
            }
        ]
        data = await mongo.aggregate(account_info.__name__, pipeline)
        print(data)

        return JSONResponse(content=UsernameLinkModel(**data[0], message=UsernameLinkMsg.is_found).model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in get_username_link_profile: {str(e)}")
        return JSONResponse(content=ErrorMessageModel(message=UsernameLinkMsg.handle_error).model_dump(mode="json"), status_code=500)