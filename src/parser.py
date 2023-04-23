import pika

from src.objects.config import config
from src.objects.logger import logger
from RbcParser import RbcParser
from src.objects.schemas import ParsedMessage

queue_consume_name = 'parse_queue'
queue_produce_name = 'download_queue'
queue_produce_elk_name = 'elk_queue'

def parse(ch, method, props, body):
    html = body.decode('utf-8')
    try:
        message: ParsedMessage = RbcParser.parse(html=html)
        logger.info(message)
        for url in message.links:
            ch.basic_publish(exchange='',
                         routing_key=queue_produce_name,
                         body=url.encode('utf-8'))
        ch.basic_publish(exchange='',
                         routing_key=queue_produce_elk_name,
                         body=message.json().encode('utf-8'))
    except Exception as e:
        logger.error(e)
    ch.basic_ack(delivery_tag=method.delivery_tag)

credentials = pika.PlainCredentials(config.RMQ_USER, config.RMQ_PASS)
parameters = pika.ConnectionParameters(config.RMQ_HOST, config.RMQ_PORT, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
queue = channel.queue_declare(queue=queue_consume_name)
channel.queue_declare(queue=queue_produce_elk_name)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_consume_name, on_message_callback=parse)
channel.start_consuming()
