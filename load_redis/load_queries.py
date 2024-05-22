from sqlalchemy import create_engine, MetaData, Table, desc, distinct
from sqlalchemy.orm import sessionmaker
from load_redis.redis_conn import r
from core.config import PG_DATABASE_URL, REDIS_QUERY_QUEUE


engine = create_engine(PG_DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


metadata = MetaData()
queries_table = Table("queries", metadata, autoload_with=engine)


def get_queries():
    query_texts = (
        session.query(distinct(queries_table.c.query_text), queries_table.c.created_at)  
        .order_by(desc(queries_table.c.created_at))
        .all()
    )

    existing_queries = set(r.smembers(REDIS_QUERY_QUEUE))

    added_count = 0

    for query_text, created_at in query_texts:
        if query_text.encode() not in existing_queries and added_count < 5:
            r.sadd(REDIS_QUERY_QUEUE, query_text)
            added_count += 1


session.close()
r.close()


if __name__ == "__main__":
    get_queries()