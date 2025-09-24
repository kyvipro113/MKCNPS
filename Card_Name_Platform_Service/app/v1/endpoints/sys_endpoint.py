from fastapi import APIRouter, Request, Depends
from Card_Name_Platform_Service.app.model.Token_Model import *
from Card_Name_Platform_Service.utils.Auth_Utility import *
from Card_Name_Platform_Service.app.model.Utils_Model import *
from Card_Name_Platform_Service.app.service.sys.utils import *
from Card_Name_Platform_Service.app.service.sys.presigned_object import *

router = APIRouter(
    prefix="/sys",
    tags=["sys"]
)

@router.get("/get-presigned-put-obj-link")
async def get_presigned_put_obj_link(request: Request, payload: PayloadEndUserModel=Depends(verify_token_factory(ObjectPresignedModel, mode="normal"))):
    ip = request.client.host
    res = await generate_presigned_put_obj_link(ip=ip, bucket_name="", is_temp=True)
    return res