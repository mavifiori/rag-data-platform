import os
from minio import Minio
from config.settings import settings

class MinioClient:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=False
        )

    def bucket_exists(self, bucket_name: str) -> bool:
        """Verifica se um bucket existe."""
        return self.client.bucket_exists(bucket_name)

    def make_bucket(self, bucket_name: str):
        """Cria um novo bucket no storage."""
        self.client.make_bucket(bucket_name)

    def put_object(self, bucket_name: str, object_name: str, data, length: int):
        """
        Faz o upload de um arquivo stream para dentro do bucket especificado.
        """
        return self.client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data,
            length=length,
            content_type="application/octet-stream"
        )

    def get_object(self, bucket_name: str, object_name: str):
        """Busca um arquivo do storage para leitura/download."""
        try:
            return self.client.get_object(bucket_name, object_name)
        except Exception as e:
            raise FileNotFoundError(f"Objeto {object_name} não encontrado no bucket {bucket_name}: {str(e)}")