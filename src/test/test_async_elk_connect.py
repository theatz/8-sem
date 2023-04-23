import asyncio
from elasticsearch import AsyncElasticsearch
from src.config import config
async def connect_elasticsearch():
    es = AsyncElasticsearch([config.ELK_URL], basic_auth=(config.ELK_USER, config.ELK_PASS))
    if await es.ping():
        print('Connected to Elasticsearch')
    else:
        print('Could not connect to Elasticsearch')
    await es.close()

async def main():
    await connect_elasticsearch()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
