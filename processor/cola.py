import pika



def consume_messages(queue_name, host='queue.altamiranofloristas.com', port=5672, username='titi', password='zxASqw!"'):
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
    
    # Definir la función de callback
    def callback(ch, method, properties, body):
        # imprimir todos los objetos de dict
        for key, value in method.__dict__.items():
            print(key, value)
    
    # Configurar el consumidor
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# Ejemplo de uso

consume_messages('1')