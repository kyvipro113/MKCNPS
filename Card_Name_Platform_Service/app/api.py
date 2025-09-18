import yaml
from fastapi import FastAPI, Depends
# Test
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.middleware.cors import CORSMiddleware

from Card_Name_Platform_Service.asyn_mongo.motor_mongo import load_settings_mongo
from Card_Name_Platform_Service.minio_client.Minio_Client import load_settings_minio
from Card_Name_Platform_Service.utils.Redis_Utility import load_settings_redis
from Card_Name_Platform_Service.utils.Send_Email import load_settings_smtp_email

from Card_Name_Platform_Service.app.router import auth_router
from Card_Name_Platform_Service.app.router import user_router



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Configure
with open("config.yaml", "r") as file:
    data = yaml.load(stream=file, Loader=yaml.Loader)

# Database
config_DB = data["DATABASE"]
DB_HOST = config_DB["DB_HOST"]
DB_PORT = config_DB["DB_PORT"]
DB_USERNAME = config_DB["DB_USERNAME"]
DB_PASSWORD = config_DB["DB_PASSWORD"] # Attention: if password use numberical seq need convert to string
DB_NAME = config_DB["DB_NAME"]

# Minio server
config_MinIO_Server = data["MINIO_SERVER_API"]
USE_PORT = config_MinIO_Server["USE_PORT"]
MSI_HOST = config_MinIO_Server["MSI_HOST"]
MSI_PORT = config_MinIO_Server["MSI_PORT"]
MINIO_SECURE = config_MinIO_Server["SECURE"]
CA_PATH = config_MinIO_Server["CA_MINIO"] if MINIO_SECURE == True else ""
ACCESS_KEY = config_MinIO_Server["ACCESS_KEY"]
SECRET_KEY = config_MinIO_Server["SECRET_KEY"]

URL_MINIO_SERVER = (MSI_HOST + ":" + str(MSI_PORT)) if USE_PORT == True else MSI_HOST

# Redis server
config_Redis = data["REDIS_SERVER"]
REDIS_HOST = config_Redis["REDIS_HOST"]
REDIS_PORT = config_Redis["REDIS_PORT"]

# Email sender
config_Email_Sender = data["EMAIL_SENDER"]
EMAIL = config_Email_Sender["EMAIL"]
KEY = config_Email_Sender["KEY"]

load_settings_mongo(DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_NAME)

if MINIO_SECURE:
    load_settings_minio(URL_MINIO_SERVER, ACCESS_KEY, SECRET_KEY, MINIO_SECURE, CA_PATH)
else:
    load_settings_minio(URL_MINIO_SERVER, ACCESS_KEY, SECRET_KEY, MINIO_SECURE)

load_settings_redis(REDIS_HOST, REDIS_PORT)

load_settings_smtp_email(EMAIL, KEY)


# Include router
app.include_router(auth_router.router)
app.include_router(user_router.router)

@app.post("/token")
async def token(request: Request, data=Depends(OAuth2PasswordRequestForm)):
    from Card_Name_Platform_Service.app.service.auth.authentication import authenticate_user, AuthModel
    print(f"{data.username, data.password}")
    ip = request.client.host
    res = await authenticate_user(auth=AuthModel(email=data.username, password=data.password), ip=ip)
    print(res)
    return res