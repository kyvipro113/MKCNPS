from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.app.model.Utils_Model import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *
from Card_Name_Platform_Service.app.model.Utils_Model import *

async def generate_presigned_put_obj_link(bucket_name: str, ip: str, object_name: str="", is_temp=False):
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    try:
        bucket_name = "temp" if is_temp else bucket_name
        print(f"bucket_name: {bucket_name}")
        await Minio_Client.create_folder(bucket_name=bucket_name)
        obj_name = ObjectIdGenerator.generate() if object_name == "" else object_name
        presigned_url  = await Minio_Client.get_url_upload(bucket_name=bucket_name, object_name=obj_name)
        presigned_model = ObjectPresignedModel(object_name=obj_name, presigned_link=presigned_url, message=MinIOMsg.successful)
        return JSONResponse(content=presigned_model.model_dump(mode="json"), status_code=200)
    except Exception as e:
        print(str(e))
        await logger.trace(f"Exception in generate_presigned_put_obj_link: {str(e)}")
        return JSONResponse(content=ObjectPresignedModel(object_name="", presigned_link="", message=MinIOMsg.failed).model_dump(mode="json"), status_code=400)
    

async def generate_presigned_get_obj_link(bucket_name: str, object_name: str, ip: str):
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    minio_client = Minio_Client()
    try:
        presigned_url  = await minio_client.get_url(bucket_name=bucket_name, object_name=object_name)
        presigned_model = ObjectPresignedModel(object_name=object_name, presigned_link=presigned_url, message=MinIOMsg.successful)
        return JSONResponse(content=presigned_model.model_dump(mode="json"), status_code=200)
    except Exception as e:
        print
        await logger.trace(f"Exception in generate_presigned_get_obj_link: {str(e)}")
        return JSONResponse(content=ObjectPresignedModel(object_name="", presigned_link="", message=MinIOMsg.failed).model_dump(mode="json"), status_code=400)