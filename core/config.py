# Local Configurations
PG_USER = "postgres"
PG_PASSWORD = "pgs24"
PG_HOST = "localhost"
PG_PORT = "5433"
PG_DB = "accountgpt"
REDIS_HOST = "localhost"
REDIS_PORT = "6379"


# Docker Configurations
# PG_USER = "accountgpt"
# PG_PASSWORD = "accountgpt"
# PG_HOST = "database"
# PG_PORT = "5432"
# PG_DB = "accountgpt"
# REDIS_HOST = "redis"
# REDIS_PORT = "6380"


# Common Configurations
GOOGLE_CSE_ID = "d04b8c862e99b466b"
GOOGLE_API_KEY = "AIzaSyCnfmOppgK4PSINQcLyyGfuZxGYuBTgvLs"

OUTPUT_FILE = "text_output"

PG_DATABASE_URL =  f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
REDIS_BROKER = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

REDIS_DB = 0
REDIS_QUERY_QUEUE = "queries"
REDIS_URL_HASH = "urls_from_google"
REDIS_PROCESSED_URL = "processed_queries_urls"

SCRAPY_SETTINGS = {
    'DOWNLOAD_DELAY': 3,
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 3,
    'CONCURRENT_REQUESTS': 20,
    'AUTOTHROTTLE_MAX_DELAY': 7,
}

