import os
from shared.storage.minio_client import MinioClient

class DataLakeLoader:
    
    def __init__(self):
        self.storage_client = MinioClient()
        self.bucket_name = "raw-documents"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """zona raw exista no MinIO."""
        try:
            if not self.storage_client.bucket_exists(self.bucket_name):
                self.storage_client.make_bucket(self.bucket_name)
                print(f"[Loading] Bucket '{self.bucket_name}' criado com sucesso.")
        except Exception as e:
            print(f"[X] Erro ao verificar/criar bucket no MinIO: {str(e)}")

    def load_to_raw_zone(self, local_file_path: str) -> str:
       
        file_name = os.path.basename(local_file_path)
        try:
            with open(local_file_path, "rb") as file_data:
                # Calcula o tamanho do arquivo para o upload
                file_stat = os.stat(local_file_path)
                
                self.storage_client.put_object(
                    bucket_name=self.bucket_name,
                    object_name=file_name,
                    data=file_data,
                    length=file_stat.st_size
                )
            print(f"[Loading] Arquivo '{file_name}' persistido na Raw Zone (MinIO).")
            return f"s3://{self.bucket_name}/{file_name}"
            
        except Exception as e:
            raise RuntimeError(f"Falha ao carregar arquivo no Data Lake: {str(e)}")