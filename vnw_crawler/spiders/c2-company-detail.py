# This spider will crawl company url --> company detail
# command:
# scrapy crawl vnw-company-detail

import re

from dacite import from_dict
from scrapy import Request

from vnw_crawler.items.CompanyItem import CompanyUrlItem, CompanyDetailItem
from .base_spider import VnwCrawlerBaseSpider, settings

class VnwCrawlerCompanyDetailSpider(VnwCrawlerBaseSpider):
    name = 'vnw-company-detail'

    def __init__(self, test=None, *args, **kwargs):
        super(VnwCrawlerBaseSpider, self).__init__(*args, **kwargs)
        self.test = test
        if test:
            self.start_urls = [
                CompanyUrlItem(
                    _id = "Star-Fashion-Crystal",
                    name= "Công ty TNHH Thời Trang Star",
                    url= "https://www.vietnamworks.com/company/Star-Fashion-Crystal"
                )
            ]

            self.logger.info("Testing")
        else:
            self.create_connection()
            self.collection_company_url = self.db[settings.get('MONGO_COLLECTION_COMPANY_URL')]

    def start_requests(self):
        if self.test:
            for cate in self.start_urls:
                yield Request(cate.url, cb_kwargs=dict(cate_url = cate))
        else:
            for cate_url in self.collection_company_url.find({}):
                cate = from_dict(data_class=CompanyUrlItem, data=cate_url)
                yield Request(cate_url['url'], cb_kwargs=dict(cate_url=cate))

    def parse(self, response, cate_url):
        company_detail = CompanyDetailItem(
            _id = cate_url._id,
            name= cate_url.name,
            company_url="",
            follow="",
            social=[]
        )

        basic_info = response.css(".cp_basic_info_details")
        info = basic_info.css("ul")
        # for item in info.css("li"):
        company_url = info.css("a.website-company::attr(href)").get()
        company_detail.company_url = company_url

        facebook = info.css("a.ic-social-facebook::attr(href)").get()
        linked = info.css("a.ic-social-linkedin::attr(href)").get()
        company_detail.social['Facebook'] = facebook
        company_detail.social['Linked'] = linked

        follower = response.css(".cp_follow_survey")
        total_follow = follower.css(".total_follow::text").get()
        company_detail.follow = total_follow

        yield company_detail