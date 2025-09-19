from fastapi.responses import JSONResponse
from Card_Name_Platform_Service.app.model.Register_Model import *
from Card_Name_Platform_Service.minio_client.Minio_Client import *
from Card_Name_Platform_Service.utils.Error_Msg import *
from Card_Name_Platform_Service.logger.Logger import *
from Card_Name_Platform_Service.utils.object_id import *

async def generate_presigned_image(ip: str):
    logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
    minio_client = Minio_Client()
    image_name = ObjectIdGenerator.generate()
    presigned_url  = await minio_client
