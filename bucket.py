from minio import Minio

# Create client with access key and secret key with specific region.
# Create client with custom HTTP client using proxy server.
client = Minio(
    "192.168.11.179:42389",  # Corregir la URL eliminando el "https://" y el "path"
    access_key="PcrmXHAXGlrD4jGhGUHM",
    secret_key="WiQsGJxNSYL4iWZQdtSPca2KTSQSAVN6VQLksWVe",
    secure=True,
)



def upload_file(bucket_name, file_path, file_name):
    # Upload file to bucket
    return client.fput_object(bucket_name, file_name, file_path)
    # return f"File uploaded successfully to {bucket_name}"

# # Get all files from bucket
# objects = client.list_objects("tempvideo")
# for obj in objects:
#     print(obj.object_name)

# # Get file from bucket
# client.fget_object("tempvideo", "jobs.mp4", "jobs.mp4")

