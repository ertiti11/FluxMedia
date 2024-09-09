from minio import Minio

# Create client with access key and secret key with specific region.
# Create client with custom HTTP client using proxy server.
client = Minio(
    "192.168.0.9:9000",  # Corregir la URL eliminando el "https://" y el "path"
    access_key="Poo44QLXd26tolTixQcN",
    secret_key="SHEgeMW106O26Nrb2Oez9Rusyu5I452DEtSDwUK1",
    secure=False,
)



def upload_file(bucket_name, file_path, file_name):
    # Upload file to bucket
    return client.fput_object(bucket_name, file_name, file_path)
    # return f"File uploaded successfully to {bucket_name}"

def get_video_from_bucket(bucket_name, object_name):
    # Get file from bucket
    local_file_path = f"/tmp/{object_name.split('/')[-1]}"  # Guardar con el nombre del archivo en /tmp
    client.fget_object(bucket_name, object_name, local_file_path)
    return local_file_path



