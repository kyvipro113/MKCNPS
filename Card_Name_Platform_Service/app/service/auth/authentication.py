import re
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from Card_Name_Platform_Service.app.model.Auth_Model import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.JWT_Utility import *
from Card_Name_Platform_Service.utils.Error_Msg import *


def is_phone_number_sequence(s):
    return bool(re.fullmatch(r'\d+', s))

async def authenticate_user(auth: AuthModel, ip: str, mode="end_user"):
    """"Two mode: end_user, cms. Default end_user"""
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    account_if = None
    token_model = TokenModel()

    if mode == "end_user":
        is_phone_number = is_phone_number_sequence(auth.email)
        try:
            if is_phone_number:
                query = {
                    "phone_number": auth.email,
                    "pwd": auth.password,
                    "act_login_by_phone_number": True
                }
                account_if = await mongo.find_one(account_info.__name__, query)
            else:
                query = {
                    "email": auth.email,
                    "pwd": auth.password,
                }    
                account_if = await mongo.find_one(account_info.__name__, query)
            print(account_if)
            print((account_if["_id"]))
            print(type(str(account_if["_id"])))
            if account_if is None:
                token_model.message = LoginMsg.user_not_found
                return JSONResponse(content=token_model.model_dump(mode="json"), status_code=401)
            
            accountIF = account_info(**account_if)
            print(type(accountIF.id))
            print(accountIF.id)

            token_data = PayloadEndUserModel(
                uid=str(accountIF.id),
                flag=accountIF.first_login,
                change_profile=accountIF.change_profile
            )

            token_model.access_token, token_model.refresh_token = create_jwt_access_and_refresh_token(data=token_data.model_dump(mode="python"))
            token_model.message = LoginMsg.successful

            print(token_model.model_dump(mode="json"))
            return JSONResponse(content=token_model.model_dump(mode="json"), status_code=200)

        except Exception as e:
            print(str(e))
            await logger.trace(f"Exception in authenticate_user: {str(e)}")
            token_model.message = LoginMsg.handle_error
            return JSONResponse(content=token_model.model_dump(mode="json"), status_code=400)
    
    else:
        try:
            query = {
                "manager_user_name": auth.email,
                "manager_pwd": auth.password,
            }
            account_if = await mongo.find_one(manager_account.__name__, query)
            
            if account_if is None:
                token_model.message = LoginMsg.cms_not_found
                return JSONResponse(content=token_model.model_dump(mode="json"), status_code=401)
            
            accountIF = manager_account(**account_if)

            token_data = PayloadManagerModel(
                uid=str(accountIF.id), 
                group_id=accountIF.group_id, 
                username=accountIF.manager_user_name, 
                name=accountIF.manager_name,
                status=accountIF.status
            )

            token_model.access_token, token_model.refresh_token = create_jwt_access_and_refresh_token(data=token_data.model_dump(mode="python"))
            token_model.message = LoginMsg.successful
            return JSONResponse(content=token_model.model_dump(mode="json"), status_code=200)

        except Exception as e:
            await logger.trace(f"Exception in authenticate_cms: {str(e)}")
            token_model.message = LoginMsg.handle_error
            return JSONResponse(content=token_model.model_dump(mode="json"), status_code=400)
    