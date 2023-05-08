import scrapy
import pymongo
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

class VnwCrawlerBaseSpider(scrapy.Spider):
    domain = 'www.vietnamworks.com'
    allowed_domains = [domain]

    def join_url(self, sub_url):
        # nếu biến đầu tiên != "/" => thêm dấu "/" vào
        if sub_url[0] != "/":
            sub_url = "/" + sub_url
        return f"https://{self.domain}{sub_url}"
    
    # tạo kết nối db
    def create_connection(self):
        conn = pymongo.MongoClient(
            settings.get('MONGO_HOST'),
            settings.get('MONGO-PORT')
        )
        self.db = conn[settings.get('MONGO_DB_NAME')]