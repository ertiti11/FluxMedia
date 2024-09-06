from redis import Redis
# def send_message(queue_name, message, host='queue.altamiranofloristas.com', port=5672, username='titi', password='zxASqw!"'):
#     # Crear credenciales
#     credentials = pika.PlainCredentials(username, password)
    
#     # Conectar usando las credenciales
#     connection = pika.BlockingConnection(pika.ConnectionParameters(
#         host,
#         port,
#         '/',
#         credentials
#     ))
    
#     channel = connection.channel()
#     channel.queue_declare(queue=queue_name)
#     channel.basic_publish(exchange='', routing_key=queue_name, body=message)
#     print(f" [x] Sent '{message}' to queue '{queue_name}'")
#     connection.close()
redis_client = Redis(
    host='54.37.51.72',
    port=6379,
    password='Wq98koIcMRUYEmBPMshA5jlGNGBcOqtzjYf0vJsjzScEvWWf6RIGhO8xAYwTSzVo',  # Reemplaza 'tu_contraseña' con la contraseña real
    decode_responses=True
)
def send_message(object):
    # Poner una tarea en la cola
    redis_client.lpush('video_transcode_queue', object)
    print(f"Tarea de transcodificación añadida a la cola: {object}")