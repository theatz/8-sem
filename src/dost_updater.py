import asyncio
from elasticsearch import AsyncElasticsearch
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from objects.config import config
from objects.logger import logger

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)


async def get_docs(size: int = 250) -> list:
    logger.info("Getting docs")
    es = AsyncElasticsearch(
        hosts=[config.ELK_URL],
        basic_auth=(config.ELK_USER, config.ELK_PASS),
    )
    query = {
        "query": {
            "bool": {
                "must": [],
                "filter": [],
                "should": [],
                "must_not": [
                    {
                        "exists": {
                            "field": "tonality"
                        }
                    }
                ]
            }
        }
    }
    documents = await es.search(index="rbc", body=query, size=size)
    logger.info(f"Found {documents['hits']['total']['value']} documents")
    logger.info(f"Returned {len(documents['hits']['hits'])} documents")
    await es.close()
    return documents['hits']['hits']

async def update_docs(documents: list) -> None:
    logger.info("Updating docs")
    es = AsyncElasticsearch(
        hosts=[config.ELK_URL],
        basic_auth=(config.ELK_USER, config.ELK_PASS),
    )
    for doc in documents:
        await es.update(index="rbc", id=doc["id"], body={"doc": {"tonality": doc["tonality"]}})
    logger.info(f"Updated {len(documents)} documents")
    await es.close()

async def main():
    docs = await get_docs(size=1000)
    update_list = []
    for doc in docs: # "body": doc["_source"].update({})
        update_list.append({"id": doc["_id"], "tonality": model.predict([doc["_source"]["body"]], k=4)})
    await update_docs(update_list)

if __name__ == "__main__":
    logger.info('Starting scheduler for dost_updater')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, 'interval', minutes=2)
    scheduler.start()
    asyncio.new_event_loop().run_forever()
