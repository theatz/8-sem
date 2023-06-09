import asyncio
import aio_pika

from src.objects.config import config
from src.objects.logger import logger

queue_name='download_queue'

async def publish_message():
    connection = await aio_pika.connect_robust(host=config.RMQ_HOST,
                                               port=config.RMQ_PORT,
                                               login=config.RMQ_USER,
                                               password=config.RMQ_PASS)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(queue_name, aio_pika.ExchangeType.DIRECT)
    message = aio_pika.Message(body=b'Hello, world!')
    await exchange.publish(message)
    await connection.close()

async def consume_message():
    connection = await aio_pika.connect_robust(host=config.RMQ_HOST,
                                               port=config.RMQ_PORT,
                                               login=config.RMQ_USER,
                                               password=config.RMQ_PASS)
    channel = await connection.channel()
    # exchange = await channel.declare_exchange(queue, aio_pika.ExchangeType.DIRECT)
    queue = await channel.declare_queue(queue_name)
    # await queue.bind(exchange, routing_key='my_routing_key')
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print(message.body.decode('utf-8'))
    await connection.close()

async def main():
    # await publish_message()
    await consume_message()

asyncio.run(main())
