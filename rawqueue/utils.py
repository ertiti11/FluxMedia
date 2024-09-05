import pika

def send_message(queue_name, message, host='queue.altamiranofloristas.com', port=5672, username='titi', password='zxASqw!"'):
    # Crear credenciales
    credentials = pika.PlainCredentials(username, password)
    
    # Conectar usando las credenciales
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host,
        port,
        '/',
        credentials
    ))
    
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print(f" [x] Sent '{message}' to queue '{queue_name}'")
    connection.close()