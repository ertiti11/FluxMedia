from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse
from bucket import upload_file, get_video_from_bucket
from rawqueue.utils import send_message
from shutil import copyfileobj
import json

app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to the videores api"


@app.post("/upload")
def upload_video(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"
    bucket_name = "tempvideo"
    
    # Guardar el archivo en el servidor
    with open(file_path, "wb") as buffer:
        copyfileobj(file.file, buffer)
    
    # Llamar a la función upload_file
    return upload_file(bucket_name, file_path, file.filename)


@app.post("/webhook")
async def handle_webhook(request: Request, payload: dict):
    # Imprimir todo el contenido del payload
    print(payload)
    payload_json = json.dumps(payload)
    print(payload_json)
    send_message(payload_json)
    
    # Puedes realizar más acciones aquí como guardar en una base de datos, etc.
    
    return {"status": "success"}


#static cdn get video from minio bucket

@app.get("/video/{video_path:path}")
def get_video(video_path: str):
    bucket_name = "videos"
    local_file_path = get_video_from_bucket(bucket_name, video_path)
    
    # Servir el archivo al cliente
    return FileResponse(local_file_path, media_type='application/vnd.apple.mpegurl')
