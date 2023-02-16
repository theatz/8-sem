import asyncio
import aiohttp
import aio_pika

from AsyncHTTPConnector import AsyncHTTPConnector
from logger import logger

class RabbitMQWebcrawler:
    def __init__(self, rabbitmq_url, queue_name, max_concurrency=10):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.max_concurrency = max_concurrency

    async def run(self, start_urls):
        # Set up RabbitMQ connection
        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        channel = await connection.channel()

        # Set up input and output queues
        input_queue = await channel.declare_queue(self.queue_name)
        output_queue = await channel.declare_queue(self.queue_name + '_results')

        # Start workers
        workers = []
        for i in range(self.max_concurrency):
            worker = asyncio.create_task(self.worker(input_queue, output_queue))
            workers.append(worker)

        # Add start URLs to input queue
        for url in start_urls:
            await input_queue.publish(aio_pika.Message(body=url.encode()))

        # Wait for workers to finish
        await asyncio.gather(*workers)

        # Close RabbitMQ connection
        await connection.close()

    async def worker(self, input_queue, output_queue):
        async with AsyncHTTPConnector() as session:
            while True:
                # Get URL from input queue
                async with input_queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        url = message.body.decode()
                        await message.ack()

                        # Make HTTP request
                        try:
                            async with session.get(url) as response:
                                if response.status == 200:
                                    body = await response.text()
                                    await output_queue.publish(aio_pika.Message(body=body.encode()))
                                else:
                                    logger.error(f"Failed to fetch {url}: {response.status}")
                        except aiohttp.ClientError as e:
                            logger.error(f"Failed to fetch {url}: {str(e)}")
