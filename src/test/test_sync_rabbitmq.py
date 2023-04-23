import time

import pika

from src.objects.config import config

# Establish a connection to RabbitMQ
credentials = pika.PlainCredentials(config.RMQ_USER, config.RMQ_PASS)
parameters = pika.ConnectionParameters(config.RMQ_HOST, config.RMQ_PORT, '/', credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# Create a queue
queue_info = channel.queue_declare(queue='download_queue')

channel.basic_publish(exchange='',
                      routing_key='download_queue',
                      body='Hello, RabbitMQ!')

# Get the queue length from the method frame
queue_length = queue_info.method.message_count
print(f'The queue length is: {queue_length}')

# Close the connection
connection.close()
