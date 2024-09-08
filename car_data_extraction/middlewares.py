import requests
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import Request
from scrapy.settings import Settings
import random
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import time

class ProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, *args, **kwargs):
        self.proxies = []
        self.failed_proxies = set()
        self.max_failed_attempts = 5
        super().__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        proxy_list_url = settings.get('PROXY_LIST_URL')

        if not proxy_list_url:
            raise NotConfigured("Proxy list URL not configured.")

        s = cls()
        s.crawler = crawler
        s.proxy_list_url = proxy_list_url
        s.update_proxies()
        crawler.signals.connect(s.update_proxies, signal=signals.spider_opened)
        crawler.signals.connect(s.log_proxies_info, signal=signals.spider_opened)
        return s

    def fetch_proxies(self):
        """Fetch proxies from the configured URL."""
        try:
            response = requests.get(self.proxy_list_url, timeout=10)
            if response.status_code == 200:
                return [proxy['ip'] + ':' + str(proxy['port']) for proxy in response.json()['data']]
            else:
                self.crawler.spider.logger.error(f"Failed to fetch proxies: HTTP {response.status_code}")
        except requests.RequestException as e:
            self.crawler.spider.logger.error(f"Error fetching proxies: {e}")
        return []

    def update_proxies(self):
        retries = 3
        for attempt in range(retries):
            self.proxies = self.fetch_proxies()
            self.failed_proxies.clear()
            if self.proxies:
                self.crawler.spider.logger.info(f"Fetched {len(self.proxies)} proxies.")
                break
            else:
                self.crawler.spider.logger.info(f"Failed to fetch proxies. Attempt {attempt + 1} of {retries}. Retrying...")
                time.sleep(2 * (attempt + 1))  # Increase delay with each retry
        if not self.proxies:
            self.crawler.engine.close_spider(self.crawler.spider, 'Failed to fetch proxies after multiple attempts.')

    def process_request(self, request, spider):
        """Set a proxy for each request."""
        if self.proxies:
            proxy = self.proxies.pop(0)  # Use the first proxy and then push it to the end of the list
            request.meta['proxy'] = f'http://{proxy}'
            self.proxies.append(proxy)
        else:
            spider.logger.warning("No proxies available, continuing without proxy.")
    
    def log_proxies_info(self, spider):
        #Log the current number of available proxies.
        spider.logger.info(f"Using {len(self.proxies)} proxies.")

# Adding random pauses
class PauseMiddleware:
    request_count = 0
    next_pause_threshold = random.randint(10, 50)  # Initial random threshold between 10 and 50 requests

    def process_request(self, request, spider):
        # Increment the request counter
        self.request_count += 1

        # Check if the current request count has reached the next pause threshold
        if self.request_count >= self.next_pause_threshold:
            # Randomly select a sleep time between 5 and 10 seconds
            sleep_time = random.uniform(5, 10)
            spider.logger.info(
                f"Pausing for {sleep_time:.2f} seconds after {self.request_count} requests."
            )
            print(
                f"Pausing for {sleep_time:.2f} seconds after {self.request_count} requests."
            )
            time.sleep(sleep_time)
            
            # Reset request count and set a new random pause threshold for the next interval
            self.request_count = 0
            self.next_pause_threshold = random.randint(10, 50)  # Randomize next pause threshold