# This spider will crawl company url --> company detail
# command:
# scrapy crawl vnw-company-detail
# scrapy crawl vnw-company-detail -a test=True

import re

from dacite import from_dict
from scrapy import Request

from vnw_crawler.items.CompanyItem import CompanyUrlItem, CompanyDetailItem
from .base_spider import VnwCrawlerBaseSpider, settings

class VnwCrawlerCompanyDetailSpider(VnwCrawlerBaseSpider):
    name = 'vnw-company-detail'

    def __init__(self, test=None, *args, **kwargs):
        super(VnwCrawlerCompanyDetailSpider, self).__init__(*args, **kwargs)
        self.test = test
        if test:
            self.start_urls = [
                CompanyUrlItem(
                    _id = "Cj-cgv",
                    name= "CJ CGV Vietnam",
                    url= "https://www.vietnamworks.com/company/Cj-cgv"
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
        basic_info = response.css(".cp_basic_info_details")
        area = ""
        company_urls = ""
        care = ""
        ul = basic_info.css("ul")
        social = []
        follower = ""
        for li in ul.css("li"):
            if li.css("a.website-company"):
                area = li.css("span::text").get()
                company_urls = li.css("a.website-company::attr(href)").get()
            else:
                care = li.css("span.li-items-limit::text").get()
                find_us = li.css("span.find-us")
                for a in find_us.css("a"):
                    content = a.css("a::attr(href)").get()
                    social.append(content)
        
        total_follow = response.css(".cp_follow_survey")
        follow = total_follow.css("span.total_follow::text").get()
        if follow:
            follower = follow.strip()
        
        address = []
        container = response.css(".cp_container_section")
        uls = container.css("ul.cp_our_office")
        for p in uls.css(".cp_address-container p"):
            content = p.css("p::text").get()
            if content is not None:
                address.append(content)
        
        yield CompanyDetailItem(
            _id = cate_url._id,
            name= cate_url.name,
            company_url=company_urls,
            career=care,
            follow=follower,
            area=area,
            social=social,
            address=address
        )
                    
        