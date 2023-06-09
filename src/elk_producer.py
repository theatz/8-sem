import asyncio
import json
import hashlib
import aio_pika
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from elasticsearch import AsyncElasticsearch

from objects.config import config
from objects.logger import logger
from objects.schemas import ParsedMessage
import searches

queue_consume_elk_name = 'elk_queue'
max_gather_size = 20


async def get_queue_length(queue_name: str = queue_consume_elk_name):
    connection = await aio_pika.connect_robust(host=config.RMQ_HOST,
                                               port=config.RMQ_PORT,
                                               login=config.RMQ_USER,
                                               password=config.RMQ_PASS)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)
    await connection.close()
    return queue.declaration_result.message_count


async def search_document(index, field, value) -> bool:
    es = AsyncElasticsearch(
        hosts=[config.ELK_URL],  # Replace with your Elasticsearch host(s)
        basic_auth=(config.ELK_USER, config.ELK_PASS),  # Optional: Provide username and password for authentication
    )

    try:
        query = searches.match_query(field=field, value=value)

        response = await es.search(index=index, body=query)
        hits = response['hits']['total']['value']

        if hits > 0:
            logger.info(f"found dublicat for {value}")
            return True
        else:
            return False

    except Exception as e:
        logger.error(f"Error occurred during search: {e}")

    await es.close()  # Close the Elasticsearch connection


async def produce_elk_doc(message: str):
    dict_message = json.loads(message)
    dublicat: bool = False

    if not dict_message.get("status", None):
        hash_md5 = hashlib.md5(dict_message["body"].encode("utf-8"))
        hash_md5 = hash_md5.hexdigest()
        dict_message.update({"md5": hash_md5})
        dublicat = await search_document(index="rbc", field="md5", value=hash_md5)

    if dublicat:
        logger.info(f"Document {dict_message['url']} already exists in Elasticsearch")
        return

    try:
        es = AsyncElasticsearch(
            hosts=[config.ELK_URL],  # Replace with your Elasticsearch host(s)
            basic_auth=(config.ELK_USER, config.ELK_PASS),  # Optional: Provide username and password for authentication
        )
        await es.index(index="rbc", document=dict_message)
        logger.info("Published doc to Elasticsearch")
    except Exception as e:
        logger.error(f"Unable to publish doc to Elasticsearch: {e}")
        raise e
    await es.close()


async def main():
    queue_length = await get_queue_length()
    logger.info(f'Queue length: {queue_length}')

    connection = await aio_pika.connect_robust(host=config.RMQ_HOST,
                                               port=config.RMQ_PORT,
                                               login=config.RMQ_USER,
                                               password=config.RMQ_PASS)

    channel = await connection.channel()
    queue = await channel.declare_queue(queue_consume_elk_name)
    messages = []

    for _ in range(min(queue_length, max_gather_size)):
        message = await queue.get()
        messages.append(message.body.decode('utf-8'))
        await message.ack()

    logger.info(f'Got {len(messages)} messages')
    await connection.close()

    tasks = []
    for message in messages:
        tasks.append(produce_elk_doc(message))
    result = await asyncio.gather(*tasks)
    logger.info(f'Produced {len(result)} messages')


if __name__ == '__main__':
    logger.info('Starting scheduler for elk_producer')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, 'interval', seconds=15)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
