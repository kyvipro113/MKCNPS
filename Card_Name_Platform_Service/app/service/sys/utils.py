from Card_Name_Platform_Service.utils.Send_Email import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.Gen_Universal_UID import *
from Card_Name_Platform_Service.utils.Redis_Utility import *
from Card_Name_Platform_Service.app.model.Utils_Model import *

body_list = [
    "Your verification code is: ",
    "Your verification code for find password is: ",
]

async def send_verification_code(code_id: str, email: str, ip: str, mode="register"):
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        print(f"Email rev: {email}")
        verify_code = genOTP_rnd()
        data_send = EmailVerifyCodeModel(email=email, verify_code=verify_code)
        client = RedisClient()
        await client.set_json(key=code_id, value=data_send.model_dump(mode="python"), ex=600)
        body = body_list[0] if mode == "register" else body_list[1]
        body += verify_code 
        Send_Email_Utility.send_mail(recipients=[email], subject="Name Card Platform Verification Code", body=body)
    except Exception as e:
        await logger.trace(f"Exception in sendVerifyCode() - {str(e)}")
        raise e


async def verify_code_check(code_id: str, email: str, verify_code: str, ip: str):
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    client = RedisClient()
    try:
        data = await client.pop_json(key=code_id)
        if data is None:
            return False
        email_verify_code = EmailVerifyCodeModel(**data)
        if email_verify_code.email != email or email_verify_code.verify_code != verify_code:
            return False
        return True
    except Exception as e:
        await logger.trace(f"Exception in verify_code_check() - {str(e)}")
        raise e

