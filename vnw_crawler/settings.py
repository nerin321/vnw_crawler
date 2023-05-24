# Scrapy settings for vnw_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'vnw_crawler'

SPIDER_MODULES = ['vnw_crawler.spiders']
NEWSPIDER_MODULE = 'vnw_crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
# #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
# #   'Accept-Language': 'en',
#     # 'cookie' : '__utmc=136564663; VNW_View = DESKTOP; ASP.NET_SessionId=zd1jrvzpk2jqxjrrmmknjvqy; ',
#     'Accept': '*/*',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Sec-Ch-Ua-Mobile': '?0',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Origin': 'https://www.vietnamworks.com//',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Dest': 'empty',
#     'Accept-Encoding': 'gzip, deflate',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'vnw_crawler.middlewares.VnwCrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'vnw_crawler.middlewares.VnwCrawlerDownloaderMiddleware': 99,
#    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware' : 100,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'vnw_crawler.pipelines.VnwCrawlerPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60 / 3
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 3 * 3
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# DUPEFILTER_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 60*60*24
HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_POLICY = 'vnw_crawler.middlewares.CachePolicy'

# mongo db settings
MONGGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB_NAME = "vnw"

MONGO_COLLECTION_COMPANY_URL = "company-url"
MONGO_COLLECTION_COMPANY_SUB_URL = "company-sub-url"
MONGO_COLLECTION_COMPANY_DETAIL = "company-detail"
MONGO_COLLECTION_EMPLOYER_DETAIL = "employer-detail"

MONGO_COLLECTION_CATEGORY_AREA = "area"
MONGO_COLLECTION_CATEGORY_RANK = "employee-rank"
MONGO_COLLECTION_CATEGORY_JOB_KIND = "job-kind"
MONGO_COLLECTION_CATEGORY_CAREER = "career"

MONGO_COLLECTION_JOB_URL = "job-url"
MONGO_COLLECTION_JOB_DETAIL = "job-detail"
