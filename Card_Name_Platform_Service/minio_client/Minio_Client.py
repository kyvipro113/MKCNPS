import aiohttp
from miniopy_async import Minio
from miniopy_async.error import *
import io
import os
import re
from datetime import timedelta

async def fetch_data(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            if response.status != 200:
                return None
            return await response.text()

class Minio_Client(object):
    URL_MINIO_SERVER: str
    ACCESS_KEY: str
    SECRET_KEY: str
    SECURE = False
    minio_client: Minio

    async def check_file_exists(bucket_name: str, object_name: str):
        folder = await Minio_Client.minio_client.bucket_exists(bucket_name=bucket_name)
        if not folder:
            await Minio_Client.minio_client.bucket_exists(bucket_name=bucket_name)
            return False
        try:
            obj = await Minio_Client.minio_client.stat_object(bucket_name=bucket_name, object_name=object_name)
            if(obj.object_name == object_name):
                return True
        except Exception as err:
            return False
        
    async def create_folder(bucket_name: str):
        folder = await Minio_Client.minio_client.bucket_exists(bucket_name=bucket_name)
        if not folder:
            await Minio_Client.minio_client.make_bucket(bucket_name=bucket_name)

    async def upload_file(bucket_name: str, object_name: str, file_path: str):
        try:
            await Minio_Client.minio_client.fput_object(bucket_name=bucket_name, object_name=object_name, file_path=file_path)
            return True
        except Exception as err:
            raise S3Error(err)

    async def upload_data(bucket_name: str, object_name: str, data: str):
        try:
            data_bytes = data.encode()
            data_stream = io.BytesIO(data_bytes)
            await Minio_Client.minio_client.put_object(bucket_name=bucket_name, object_name=object_name, data=data_stream, length=len(data_bytes))
            return True
        except Exception as err:
            raise S3Error(err)

            
        
    async def upload_data_byte(bucket_name: str, object_name: str, data: bytes, content_type="image/png"):
        try:
            data_stream = io.BytesIO(data)
            await Minio_Client.minio_client.put_object(bucket_name=bucket_name, object_name=object_name, data=data_stream, length=len(data), content_type=content_type)
            return True
        except Exception as err:
            raise S3Error(err)
        
        
    async def delete_file(bucket_name: str, object_name: str, optional=False):
        try:
            await Minio_Client.minio_client.remove_object(bucket_name=bucket_name, object_name=object_name)
            return True
        except Exception as err:
            if optional:
                pass
            raise S3Error(err)
    
    async def delete_multi_file(bucket_name: str, object_list: list):
        try:
            for object_name in object_list:
                await Minio_Client.minio_client.remove_object(bucket_name=bucket_name, object_name=object_name)
            return True
        except Exception as err:
            raise S3Error(err)
        
    async def delete_multi_file_native(bucket_name: str, object_list: list):
        try:
            await Minio_Client.minio_client.remove_objects(bucket_name=bucket_name, delete_object_list=object_list)
            return True
        except Exception as err:
            raise S3Error(err)
        
    async def download_sdata(bucket_name, object_name):
        '''Using for small text data'''
        try:
            async with aiohttp.ClientSession() as session: 
                response = await Minio_Client.minio_client.get_object(session=session, bucket_name=bucket_name, object_name=object_name)
            data = await response.read()
            response.close()
            data = bytes(data).decode("utf-8")
            return data
        except Exception as err:
            raise S3Error(err)   

    async def get_url(bucket_name, object_name):
        try:
            url = await Minio_Client.minio_client.presigned_get_object(bucket_name=bucket_name, object_name=object_name, expires=timedelta(days=1))
            return url
        except Exception as err:
            raise S3Error("MinIO Server Error:" + str(err))

    async def get_url_upload(bucket_name, object_name):
        print(f"Pre")
        try:
            print(f"Pre1")
            url = await Minio_Client.minio_client.presigned_put_object(bucket_name=bucket_name, object_name=object_name, expires=timedelta(minutes=5))
            print(f"Pre2")
            return url
        except Exception as err:
            print(f"Re")
            print(str(err))
            raise S3Error("MinIO Server Error:" + str(err))

    async def get_url_no_presign(bucket_name, object_name):
        pre_link = ""
        if Minio_Client.SECURE:
            if not Minio_Client.URL_MINIO_SERVER.startswith(("https://")):
                pre_link = "https://" + Minio_Client.URL_MINIO_SERVER
            else:
                pre_link = Minio_Client.URL_MINIO_SERVER
        else:
            if not Minio_Client.URL_MINIO_SERVER.startswith(("http://")):
                pre_link = "http://" + Minio_Client.URL_MINIO_SERVER
            else:
                pre_link = Minio_Client.URL_MINIO_SERVER
        return pre_link + "/" + bucket_name + "/" + object_name
        
    async def download_data(bucket_name, object_name):
        '''Using for large text data'''
        try:
            url = await Minio_Client.minio_client.presigned_get_object(bucket_name=bucket_name, object_name=object_name)
            data = await fetch_data(url=url)
            if data is None:
                return ""
            return data
        except Exception as err:
            raise S3Error("MinIO Server Error:" + str(err))
        

    async def move_object(src_bucket, src_object, dest_bucket, dest_object=None, remove_src=False):
        if dest_object is None:
            dest_object = src_object
        try:
            copy_src = f"{src_bucket}/{src_object}"
            await Minio_Client.minio_client.copy_object(bucket_name=dest_bucket, object_name=dest_object, object_source=copy_src)
            if remove_src:
                await Minio_Client.minio_client.remove_object(bucket_name=src_bucket, object_name=src_object)
        except Exception as err:
            raise S3Error("MinIO Server Error:" + str(err))



def is_valid_url(url):
    regex = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None

    
def load_settings_minio(URL_MINIO_SERVER, ACCESS_KEY, SECRET_KEY, SECURE=False, CA_path=""):
    print(f"Load MinIO settings, URL: {URL_MINIO_SERVER}, AccessKey: {ACCESS_KEY}, SecretKey: {SECRET_KEY} Secure: {SECURE}, CA_path: {CA_path}")
    Minio_Client.URL_MINIO_SERVER = URL_MINIO_SERVER
    Minio_Client.ACCESS_KEY = ACCESS_KEY
    Minio_Client.SECRET_KEY = SECRET_KEY
    Minio_Client.SECURE = SECURE
    if(SECURE):
        os.environ["SSL_CERT_FILE"] = CA_path
        Minio_Client.minio_client = Minio(endpoints=Minio_Client.URL_MINIO_SERVER, 
                                        access_key=Minio_Client.ACCESS_KEY, 
                                        secret_key=Minio_Client.SECRET_KEY, secure=True)
    else:
        Minio_Client.minio_client = Minio(endpoint=Minio_Client.URL_MINIO_SERVER, 
                                        access_key=Minio_Client.ACCESS_KEY, 
                                        secret_key=Minio_Client.SECRET_KEY, secure=False)
        