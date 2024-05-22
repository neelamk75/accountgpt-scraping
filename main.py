from celery import Celery
from datetime import timedelta
from tasks.task import scrape_task, load_urls_task, load_queries_task, update_vector_db
from core.config import REDIS_BROKER


app = Celery("accountgpt", broker=REDIS_BROKER)


# Run the pipeline every 3 days
app.conf.update(
    result_backend=REDIS_BROKER,
    beat_schedule={
        "load_queries": {
            "task": "tasks.task.load_queries_task",
            "schedule": timedelta(days=3)
        },
        "load_urls": {
            "task": "tasks.task.load_urls_task",
            "schedule": timedelta(days=3)
        },
        "scrape": {
            "task": "tasks.task.scrape_task",
            "schedule": timedelta(days=3) 
        },
        "update_vector": {
            "task": "tasks.task.update_vector",
            "schedule": timedelta(days=3)
        }
    },
)


if __name__ == "__main__":
    app.worker_main(["worker", "-B", "--loglevel=INFO"])
