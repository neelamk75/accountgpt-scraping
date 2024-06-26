import hashlib
import json
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.http import Request
from core.config import REDIS_URL_HASH, REDIS_PROCESSED_URL, SCRAPY_SETTINGS
from load_redis.redis_conn import r
from bs4 import BeautifulSoup
from core.config import OUTPUT_FILE
import io


class MySpider(Spider):
    name = 'my_spider'

    def start_requests(self):
        all_queries = r.hkeys(REDIS_URL_HASH)
        queries_processed_count = 0

        for query_bytes in all_queries:
            # Scrape data for 10 queries
            if queries_processed_count >= 5:
                break

            query = query_bytes.decode('utf-8')
            urls_data_json = r.hget(REDIS_URL_HASH, query)
            urls_data = json.loads(urls_data_json)

            processed_urls_data_json = r.hget(REDIS_PROCESSED_URL, query)
            processed_urls_data = json.loads(processed_urls_data_json) if processed_urls_data_json else {}

            any_url_processed = False

            for url in urls_data:
                last_modified = processed_urls_data.get(url, None)
                headers = {}
                if last_modified:
                    headers['If-Modified-Since'] = last_modified

                yield Request(url, callback=self.parse, meta={'query': query, 'url': url}, headers=headers)
                any_url_processed = True

            if any_url_processed:
                queries_processed_count += 1


    def parse(self, response):
        query = response.meta['query']
        url = response.meta['url']

        last_modified_header = response.headers.get('Last-Modified')
        if last_modified_header:
            last_modified = last_modified_header.decode('utf-8')

            processed_urls_data_json = r.hget(REDIS_PROCESSED_URL, query)
            processed_urls_data = json.loads(processed_urls_data_json) if processed_urls_data_json else {}

            if url in processed_urls_data:
                if last_modified == processed_urls_data[url]:
                    self.log(f"Content not modified for URL: {url}")
                    # Terminate scraping for this URL as content hasn't changed
                    return

            # Update last-modified date in Redis
            processed_urls_data[url] = last_modified
            r.hset(REDIS_PROCESSED_URL, query, json.dumps(processed_urls_data))

        soup = BeautifulSoup(response.text, 'html.parser')
        content = ''
        irrelevant_phrases = ['All Rights Reserved', ' All rights reserved', 'Privacy Policy', 'Terms of Use',
                            'Join Our Mailing List', 'Related Information', 'Related Topics',
                            'Footer', 'Subfooter', 'Contact us',
                            'An official website of the United States government.',
                            'Follow us']

        def is_irrelevant(text):
            return any(phrase in text for phrase in irrelevant_phrases)

        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in headings:
            heading_text = heading.get_text().strip()
            if not is_irrelevant(heading_text):
                content += f"# {heading_text}\n\n" 
                # Find paragraphs associated with the current heading
                paragraphs = heading.find_all_next(['p'])
                for paragraph in paragraphs:
                    paragraph_text = paragraph.get_text().strip()
                    if not is_irrelevant(paragraph_text) and paragraph_text:
                        content += f"{paragraph_text}\n\n" 

        self.process_content(response, content)
        
    def process_content(self, response, content):
        query = response.meta['query']
        query_hash = hashlib.sha256(query.encode('utf-8')).hexdigest()
        markdown_file_path = f'{OUTPUT_FILE}/{query_hash}.md'
        with open(markdown_file_path, 'a', encoding='utf-8') as markdown_file:
            markdown_file.write(content)


def run_spider():
    process = CrawlerProcess(SCRAPY_SETTINGS)
    process.crawl(MySpider)
    process.start()


if __name__ == "__main__":
    run_spider()
