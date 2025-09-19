from fastapi import APIRouter, Request
from Card_Name_Platform_Service.app.v1.endpoints.auth_endpoint import router as auth_router
from Card_Name_Platform_Service.app.v1.endpoints.user_endpoint import router as user_router
# from Card_Name_Platform_Service.app.v1.endpoints.cms_endpoint
from Card_Name_Platform_Service.app.v1.endpoints.profile_enpoint import router as profile_router

router = APIRouter(
    prefix="/v1"
)

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(profile_router)
