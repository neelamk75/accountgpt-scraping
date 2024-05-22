from core.config import REDIS_QUERY_QUEUE, REDIS_URL_HASH
# from search_api.custom_search import GoogleSearchAPIWrapper
from search_api.custom_search import GoogleSerperAPIWrapper
from load_redis.redis_conn import r
import json


# google_api_wrapper = GoogleSearchAPIWrapper()

google_serper_api = GoogleSerperAPIWrapper()


def get_urls():
    all_queries = r.smembers(REDIS_QUERY_QUEUE)
    queries = []
    for query in all_queries:
        if not r.hexists(REDIS_URL_HASH, query):
            queries.append(query)

    for query in queries:
        # results = google_api_wrapper.run(query)
        results = google_serper_api.run(query)
        urls = [result['link'] for result in results if isinstance(result, dict) and 'link' in result]
        urls = json.dumps(urls)
        if urls:
            r.hset(REDIS_URL_HASH, query, urls)


if __name__ == "__main__":
    get_urls()