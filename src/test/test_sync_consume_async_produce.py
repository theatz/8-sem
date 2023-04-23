import pika
import asyncio
import aiohttp

from src.objects.config import config
from src.objects.logger import logger


async def get(url: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(get) as response:
            # Retrieve the response body as text
            response_text = await response.text()
            logger.info(f"get response: {response_text[:50]}")

# Establish a connection to RabbitMQ
credentials = pika.PlainCredentials(config.RMQ_USER, config.RMQ_PASS)
parameters = pika.ConnectionParameters(config.RMQ_HOST, config.RMQ_PORT, '/', credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

queue='download_queue'

# Create a queue
queue_info = channel.queue_declare(queue=queue)

for method_frame, properties, body in channel.consume(queue):
    # Decode the message body
    message = body.decode('utf-8')

    # Print the message to the console
    logger.info(f"get message: {message}")
    asyncio.create_task(get(url=message))

    # Acknowledge that the message has been received and processed
    channel.basic_ack(method_frame.delivery_tag)

# Close the connection
connection.close()