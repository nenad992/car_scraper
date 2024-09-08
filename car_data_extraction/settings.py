BOT_NAME = 'car_data_extraction'
SPIDER_MODULES = ['car_data_extraction.spiders']
NEWSPIDER_MODULE = 'car_data_extraction.spiders'
ROBOTSTXT_OBEY = True

# Pipelines
ITEM_PIPELINES = {
    'car_data_extraction.pipelines.CarDataPipeline': 300,
}

# Concurrency settings
CONCURRENT_REQUESTS = 32  # Increase the number of concurrent requests globally PREVIOUS 32
CONCURRENT_REQUESTS_PER_DOMAIN = 4  # Number of requests per domain PREVIOUS 8
CONCURRENT_REQUESTS_PER_IP = 4  # Number of requests per IP (useful if you're scraping multiple sites) PREVIOUS 8

# Request delays
DOWNLOAD_DELAY = 1  # Adjust delay between requests; set to a lower value if server allows PREVIOUS 0.3

# AutoThrottle settings to dynamically adjust download delay based on server load
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5  # Initial delay in seconds PREVIOUS 0.5
AUTOTHROTTLE_MAX_DELAY = 12  # Maximum delay to avoid overloading servers PREVIOUS 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0  # Target concurrency level (adjust based on server capabilities) PREVIOUS 2.0
AUTOTHROTTLE_DEBUG = False  # Set to True if you want to see throttling stats

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 2  # Number of retries if a request fails
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]  # List of HTTP codes to trigger a retry

# Timeout settings
DOWNLOAD_TIMEOUT = 15  # Maximum time (in seconds) to wait for a response from the server
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7' # Added based on errors from info logs

# Cache settings to prevent hitting the same page multiple times if it hasn't changed
HTTPCACHE_ENABLED = True    
HTTPCACHE_EXPIRATION_SECS = 300  # Cache expiration time in seconds
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [200, 302, 500, 502, 503, 504, 408]  # Ignore cache for these error codes
HTTPCACHE_ALWAYS_STORE = True  # Always store requests in cache even if they fail
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy' # Ensure real-time validation to check if the cache is up-to-date
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# User-Agent rotation (consider adding more user agents if needed)
USER_AGENT = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/116.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.4; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.4; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.0.0 Safari/537.36',
]
# Proxy URL (Add valid proxy list bellow)
# PROXY_LIST_URL = 'https://proxylist.geonode.com/api/proxy-list?speed=fast&limit=500&page=1&sort_by=lastChecked&sort_type=desc'

# Middleware settings
DOWNLOADER_MIDDLEWARES = {
    'car_data_extraction.middlewares.ProxyMiddleware': 543,  # Proxy first
    'car_data_extraction.middlewares.PauseMiddleware': 550,  # Pause middleware next
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # Disabling default User-Agent middleware
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,  # Randomize User-Agent
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,  # Optional: Custom retry
}

DOWNLOADER_CLIENT_TLS_METHOD = 'TLS'
DOWNLOADER_CLIENT_TLS_VERIFY = False
DOWNLOADER_CLIENT_TLS_VERBOSE_LOGGING = True

# Logging level
LOG_LEVEL = 'INFO'  # Set to 'DEBUG' if you want more detailed logs during development
LOG_FILE = 'scrapy_log.txt'  # Define the log file location and name
