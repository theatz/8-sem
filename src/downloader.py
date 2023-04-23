import asyncio
import aio_pika
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from objects.config import config
from objects.logger import logger
from objects.AsyncHTTPConnector import AsyncHTTPConnector as HTTPConnector

queue_consume_name = 'download_queue'
queue_produce_name = 'parse_queue'

max_gather_size = 20


async def get_queue_length(queue_name: str = queue_consume_name):
    connection = await aio_pika.connect_robust(host=config.RMQ_HOST,
                                               login=config.RMQ_USER,
                                               password=config.RMQ_PASS)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)
    await connection.close()
    return queue.declaration_result.message_count

async def download(url: str) -> str | None:
    async with HTTPConnector() as connectror:
        try:
            return await connectror.request(method='GET', url=url)
        except Exception as e:
            logger.error(e)
            return None

async def main():
    queue_length = await get_queue_length()
    logger.info(f'Queue length: {queue_length}')

    connection = await aio_pika.connect_robust(host=config.RMQ_HOST,
                                               login=config.RMQ_USER,
                                               password=config.RMQ_PASS)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_consume_name)
    messages = []

    for _ in range(min(queue_length, max_gather_size)):
        message = await queue.get()
        messages.append(message.body.decode('utf-8'))
        await message.ack()

    logger.info(f'Got {len(messages)} messages: {messages}')
    await connection.close()

    tasks = []
    for message in messages:
        tasks.append(download(message))
    res = await asyncio.gather(*tasks)
    logger.info(f'Downloaded {len(res)} ulrs')

    connection = await aio_pika.connect_robust(host=config.RMQ_HOST,
                                               login=config.RMQ_USER,
                                               password=config.RMQ_PASS)
    channel = await connection.channel()
    await channel.declare_queue(queue_produce_name)

    for html in res:
        await channel.default_exchange.publish(aio_pika.Message(body=bytes(html, 'utf-8')),
                                               routing_key=queue_produce_name)
    await connection.close()

if __name__ == "__main__":
    print('Starting scheduler for downloader')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, 'interval', seconds=3)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
