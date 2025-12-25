from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Account_Info_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *

async def activate_deactivate_phone_login(data: AccountSettingsModel, payload: PayloadEndUserModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        query = {
            "_id": ObjectId(payload.uid),
            "phone_number": data.phone_number
        }
        update = {
            "act_login_by_phone_number": data.act_login_by_phone_number
        }
        await mongo.update_many(account_info.__name__, query, update)

        data.message = AccountSettingsMsg.update_account_successful

        return JSONResponse(content=data.model_dump(mode="json"), status_code=200)
    
    except Exception as e:
        print(str(e))
        data.message = AccountSettingsMsg.handle_error
        await logger.trace(f'Exception in activate_deactivate_phone_login: {str(e)}')
        return JSONResponse(content=data.model_dump(mode="json"), status_code=500)
