import aiohttp
from miniopy_async import Minio
import io

class Minio_Client(object):
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

    async def upload_data(bucket_name: str, object_name: str, data: str):
        try:
            data_bytes = data.encode()
            data_stream = io.BytesIO(data_bytes)
            await Minio_Client.minio_client.put_object(bucket_name=bucket_name, object_name=object_name, data=data_stream, length=len(data_bytes))
            return True
        except Exception as err:
            raise ValueError(err)
        
    async def delete_file(bucket_name: str, object_name: str, optional=False):
        try:
            await Minio_Client.minio_client.remove_object(bucket_name=bucket_name, object_name=object_name)
            return True
        except Exception as err:
            if optional:
                pass
            raise ValueError(err)
    
    async def delete_multi_file(bucket_name: str, object_list: list):
        try:
            for object_name in object_list:
                await Minio_Client.minio_client.remove_object(bucket_name=bucket_name, object_name=object_name)
            return True
        except Exception as err:
            raise ValueError(err)
        
    async def delete_multi_file_native(bucket_name: str, object_list: list):
        try:
            await Minio_Client.minio_client.remove_objects(bucket_name=bucket_name, delete_object_list=object_list)
            return True
        except Exception as err:
            raise ValueError(err)
        
    async def download_data(bucket_name, object_name):
        try:
            async with aiohttp.ClientSession() as session: 
                response = await Minio_Client.minio_client.get_object(session=session, bucket_name=bucket_name, object_name=object_name)
            data = await response.read()
            response.close()
            data = bytes(data).decode("utf-8")
            return data
        except Exception as err:
            raise ValueError(err)       


def load_settings_minio(URL_MINIO_SERVER, ACCESS_KEY, SECRET_KEY, SECURE=False):
    # Minio_Client.URL_MINIO_SERVER = URL_MINIO_SERVER
    # Minio_Client.ACCESS_KEY = ACCESS_KEY
    # Minio_Client.SECRET_KEY = SECRET_KEY
    # Minio_Client.SECURE = SECURE
    Minio_Client.minio_client = Minio(endpoint=URL_MINIO_SERVER, 
                                      access_key=ACCESS_KEY, 
                                      secret_key=SECRET_KEY, secure=SECURE)
        