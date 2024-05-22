from celery import Celery
import subprocess
from core.config import REDIS_BROKER
from update_vector.raptor import RaptorPack


app = Celery("accountgpt", broker=REDIS_BROKER)
raptor_pack = RaptorPack()


@app.task
def load_queries_task():
    subprocess.run(["python", "load_redis/load_queries.py"])


@app.task
def load_urls_task():
    subprocess.run(["python", "load_redis/load_urls.py"])


@app.task
def scrape_task():
    subprocess.run(["python", "load_redis/scrapy_spider.py"])


# @app.task
# def update_vector_db():
#     subprocess.run(["python", "update_vector/raptor.py"])






