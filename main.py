from fastapi import FastAPI, UploadFile, File, Request
from bucket import upload_file
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