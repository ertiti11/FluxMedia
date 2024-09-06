import redis
import time
import json
from minio import Minio
import subprocess
import re
import os

redis_client = redis.Redis(
    host='54.37.51.72',
    port=6379,
    password='Wq98koIcMRUYEmBPMshA5jlGNGBcOqtzjYf0vJsjzScEvWWf6RIGhO8xAYwTSzVo',
    decode_responses=True
)

minio_client = Minio(
    "127.0.0.1:9000",
    access_key="kzUDMubKlxIH4JCHMpr5",
    secret_key="B4OsaThNm8MIXGaf5arLkzTcoSnzsReNqMBQuInn",
    secure=False,
)

def get_video_duration(video_file):
    """Obtén la duración del video en segundos usando ffprobe"""
    command = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', video_file
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def video_to_stream(video_file):
    """Convierte MP4 a HLS y muestra el porcentaje de progreso."""
    # Obtén la duración del video para calcular el porcentaje de progreso
    duration = get_video_duration(video_file)
    
    # Crear un nombre de directorio para los archivos HLS
    base_name = os.path.splitext(video_file)[0]
    output_dir = base_name
    
    # Crear directorio si no existe
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    # Comando de FFmpeg para convertir MP4 a HLS
    command = [
        'ffmpeg',
        '-i', video_file,
        '-profile:v', 'baseline',
        '-level', '3.0',
        '-start_number', '0',
        '-hls_time', '10',
        '-hls_list_size', '0',
        '-f', 'hls',
        f'{output_dir}/{base_name}.m3u8'
    ]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Expresión regular para extraer el tiempo procesado del video
    time_regex = re.compile(r'time=(\d+:\d+:\d+\.\d+)')
    
    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # Extraer el tiempo procesado del video
            match = time_regex.search(output)
            if match:
                time_str = match.group(1)
                # Convertir el tiempo procesado a segundos
                h, m, s = map(float, time_str.split(':'))
                processed_time = h * 3600 + m * 60 + s
                # Calcular el porcentaje
                percentage = (processed_time / duration) * 100
                print(f"Progreso: {percentage:.2f}%")
    
    # Subir el archivo .m3u8 y todos los segmentos al bucket de MinIO
    minio_client.fput_object("videos", f"{output_dir}/{base_name}.m3u8", f"{output_dir}/{base_name}.m3u8")
    
    # Subir todos los segmentos HLS al bucket de MinIO
    for segment in os.listdir(output_dir):
        if segment.endswith(".ts"):
            segment_path = os.path.join(output_dir, segment)
            minio_client.fput_object("videos", f"{output_dir}/{segment}", segment_path)
    
    return process.poll()

def get_video_file(video_file):
    """Obtén el archivo de video del bucket de MinIO."""
    print("Obteniendo archivo de video...")
    minio_client.fget_object("tempvideo", video_file, video_file)

def process_video_task():
    """Procesa las tareas de video en la cola."""
    print("Esperando mensajes en la cola 'video_transcode_queue'...")
    while True:
        task = redis_client.brpop('video_transcode_queue')
        video_file = task[1]
        print("Contenido recibido de la cola")
        try:
            video_data = json.loads(video_file)
            video_key = video_data["Records"][0]["s3"]["object"]["key"]
            get_video_file(video_key)
            video_to_stream(video_key)
        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
        time.sleep(5)

process_video_task()
