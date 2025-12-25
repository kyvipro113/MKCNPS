from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.asyn_mongo.motor_mongo import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.utils.Send_Email import *
from Card_Name_Platform_Service.utils.Gen_Universal_UID import *
from Card_Name_Platform_Service.utils.Redis_Utility import *
from Card_Name_Platform_Service.utils.JWT_Utility import *
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.app.service.sys.utils import *

async def find_password_endpoint(email: str, ip: str):
    mongo = AsyncMongoDB()

    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        pipeline = [
            {
                "$match": {
                    "email": email
                }
            },
            {
                "$project": {
                    "_id": 1
                }
            }
        ]
        data = await mongo.aggregate(account_info.__name__, pipeline)
        if data is None or len(data) == 0:
            return JSONResponse(content=TokenModel(message=ForgotPasswordMsg.email_not_found).model_dump(mode="json"), status_code=499)
        
        id = str(data[0]["_id"])
        code_id = str(uuid.uuid4())
        
        await send_verification_code(code_id=code_id, email=email, ip=ip, mode="forgot_password")

        token_data = PayloadEndUserModel(
            uid=id,
            email=email,
            code_id=code_id
        )

        token_model = TokenModel()
        token_model.access_token = await create_jwt_token(data=token_data.model_dump(mode="python"))
        token_model.message = ForgotPasswordMsg.send_email_successful
        await logger.info(f"Forgot password email sent to {email} from IP: {ip}")
        return JSONResponse(content=token_model.model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in forgot_password_endpoint - : {str(e)}")
        return JSONResponse(content=TokenModel(message=ForgotPasswordMsg.send_email_failed).model_dump(mode="json"), status_code=400)
    

async def reset_password_endpoint(payload: PayloadEndUserModel, verify_code: str, new_password: str, ip: str):
    mongo = AsyncMongoDB()
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        print(payload)
        verified = await verify_code_check(code_id=payload.code_id, email=payload.email, verify_code=verify_code, ip=ip)
        if not verified:
            return JSONResponse(content=TokenModel(message=ResetPasswordMsg.invalid_verify_code).model_dump(mode="json"), status_code=493)
        
        update = {"pwd": new_password}
        result = await mongo.update_one(account_info.__name__, payload.uid, update)
        print(f"Update result: {result}")
        await logger.info(f"Password reset successful for user ID: {str(payload.uid)} from IP: {ip}")
        return JSONResponse(content=TokenModel(message=ResetPasswordMsg.reset_password_successful).model_dump(mode="json"), status_code=200)

    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in reset_password_endpoint - : {str(e)}")
        return JSONResponse(content=TokenModel(message=ResetPasswordMsg.reset_password_failed).model_dump(mode="json"), status_code=400)


