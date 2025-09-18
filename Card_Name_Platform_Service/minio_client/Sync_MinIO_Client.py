from minio import Minio
from minio.error import InvalidResponseError, S3Error
import io


class Sync_Minio_Client(object):
    URL_MINIO_SERVER: str
    ACCESS_KEY: str
    SECRET_KEY: str
    SECURE = False

    def __init__(self):
        print(Sync_Minio_Client.URL_MINIO_SERVER)
        print(Sync_Minio_Client.ACCESS_KEY)
        print(Sync_Minio_Client.SECRET_KEY)
        print(Sync_Minio_Client.SECURE)
        self.minio_client = Minio(endpoint=Sync_Minio_Client.URL_MINIO_SERVER, 
                                  access_key=Sync_Minio_Client.ACCESS_KEY, 
                                  secret_key=Sync_Minio_Client.SECRET_KEY, secure=Sync_Minio_Client.SECURE)
        
    def check_file_exists(self, bucket_name, object_name):
        folder = self.minio_client.bucket_exists(bucket_name=bucket_name)
        if not folder:
            self.minio_client.make_bucket(bucket_name=bucket_name)
            return False
        try:
            obj = self.minio_client.stat_object(bucket_name=bucket_name, object_name=object_name)
            if(obj.object_name == object_name):
                return True
            else:
                return False 
        except S3Error as err:
            print(str(err))
            return False
        
    def create_folder(self, bucket_name):
        folder = self.minio_client.bucket_exists(bucket_name=bucket_name)
        if not folder:
            self.minio_client.make_bucket(bucket_name=bucket_name)

    def upload_data(self, bucket_name, object_name, data):
        '''
        bucket_name as folder name
        object_name as file name
        '''
        try:
            data_bytes = data.encode()
            data_stream = io.BytesIO(data_bytes)
            self.minio_client.put_object(bucket_name=bucket_name, object_name=object_name, data=data_stream, length=len(data_bytes))
            return True
        except S3Error as err:
            raise ValueError(err)
        except InvalidResponseError as err:
            raise ValueError(err)
        
    def delete_file(self, bucket_name, object_name, optional=False):
        '''
        bucket_name as folder name
        object_name as file name
        optional for rollback when create job error in db but create object success in minio server
        '''
        try:
            self.minio_client.remove_object(bucket_name=bucket_name, object_name=object_name)
            return True
        except S3Error as err:
            if optional:
                pass
            raise ValueError(err)
        except InvalidResponseError as err:
            if optional:
                pass
            raise ValueError(err)
        
    def delete_multi_file(self, bucket_name, object_list):
        '''
        bucket_name as folder name
        object_list as list file name of list file need delete
        '''
        try:
            self.minio_client.remove_objects(bucket_name=bucket_name, delete_object_list=object_list)
            return True
        except S3Error as err:
            raise ValueError(err)
        except InvalidResponseError as err:
            raise ValueError(err)

    def upload_file(self, bucket_name, object_name, file_path):
        folder = self.minio_client.bucket_exists(bucket_name=bucket_name)
        if not folder:
            self.minio_client.make_bucket(bucket_name=bucket_name)
        try:
            self.minio_client.fget_object(bucket_name=bucket_name, object_name=object_name, file_path=file_path)
            return True

        except S3Error as err:
            raise ValueError(err)
        except InvalidResponseError as err:
            raise ValueError(err)

    def download_data(self, bucket_name, object_name):
        try:
            response = self.minio_client.get_object(bucket_name=bucket_name, object_name=object_name)
            data = response.data.decode("utf-8")
            return data
        except Exception as err:
            raise ValueError(err)
            


def load_settings_minio_sync(URL_MINIO_SERVER, ACCESS_KEY, SECRET_KEY, SECURE=False):
    Sync_Minio_Client.URL_MINIO_SERVER = URL_MINIO_SERVER
    Sync_Minio_Client.ACCESS_KEY = ACCESS_KEY
    Sync_Minio_Client.SECRET_KEY = SECRET_KEY
    Sync_Minio_Client.SECURE = SECURE
