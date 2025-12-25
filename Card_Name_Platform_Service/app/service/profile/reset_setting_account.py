from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.model.Account_Info_Model import *
from Card_Name_Platform_Service.app.service.sys.utils import *

async def reset_setting_account(data: ResetSettingsModel, payload: PayloadEndUserModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try: 
        match data.flag:
            case 0:
                # Reset phone number
                reset_phone = data.phone_number if data.phone_number else ""

                if not reset_phone:
                    data.message = AccountSettingsMsg.reset_setting_invalid_phone_number
                    return JSONResponse(content=data.model_dump(mode="json"), status_code=499)

                update = {
                    "phone_number": reset_phone
                }
                await mongo.update_one(account_info.__name__,payload.uid, update)

            case 1:
                # Reset email
                reset_email = data.email if data.email else ""

                if not reset_email:
                    data.message = AccountSettingsMsg.reset_setting_invalid_email
                    return JSONResponse(content=data.model_dump(mode="json"), status_code=499)

                verified = await verify_code_check(code_id=payload.uid, email=reset_email, verify_code=data.otp, ip=ip)
                if not verified:
                    data.message = AccountSettingsMsg.invalid_otp
                    return JSONResponse(content=data.model_dump(mode="json"), status_code=498)

                update = {
                    "email": reset_email
                }
                await mongo.update_one(account_info.__name__, payload.uid, update)
            
            case 2:
                # Reset password
                old_password = data.old_password if data.old_password else ""
                reset_password = data.new_password if data.new_password else ""

                if (not old_password or not reset_password 
                    or not old_password.strip() or not reset_password.strip()):
                    data.message = AccountSettingsMsg.reset_setting_invalid_password
                    return JSONResponse(content=data.model_dump(mode="json"), status_code=499)

                query = {
                    "_id": ObjectId(payload.uid),
                    "pwd": old_password
                }
                update = {
                    "pwd": reset_password
                }
                await mongo.update_many(account_info.__name__, query, update)

            case _:
                data.message = AccountSettingsMsg.invalid_flag
                return JSONResponse(content=data.model_dump(mode="json"), status_code=499)
        
        data.message = AccountSettingsMsg.reset_setting_successful
        return JSONResponse(content=data.model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        data.message = AccountSettingsMsg.reset_setting_failed
        await logger.trace(f'Exception in reset_phone_setting_account - : {str(e)}')
        return JSONResponse(content=data.model_dump(mode="json"), status_code=500)
    

async def send_verify_code(data: ResetSettingsModel, payload: PayloadEndUserModel, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        email = data.email if data.email else ""
        if not email:
            data.message = AccountSettingsMsg.email_not_found
            return JSONResponse(content=data.model_dump(mode="json"), status_code=499)
    
        account = await mongo.find_one_id(account_info.__name__,payload.uid)
        if account is None:
            data.message = AccountSettingsMsg.not_found
            return JSONResponse(content=data.model_dump(mode="json"), status_code=498)
        
        await send_verification_code(code_id=payload.uid, email=email, ip=ip)
        data.message = AccountSettingsMsg.send_verify_code_successful
        return JSONResponse(content=data.model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        data.message = AccountSettingsMsg.send_verify_code_failed
        await logger.trace(f'Exception in send_verify_code - : {str(e)}')
        return JSONResponse(content=data.model_dump(mode="json"), status_code=500)



