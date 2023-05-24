# This spider will crawl company sub url --> company detail
# command:
# while True:
# scrapy crawl vnw-sub-to-company -a test=True

import re
from dacite import from_dict
from scrapy import Request

from vnw_crawler.items.CompanyItem import CompanySubUrlItem, CompanySubDetailItem
from .base_spider import VnwCrawlerBaseSpider, settings

class VnwCrawlerSubCompanySpider(VnwCrawlerBaseSpider):
    name = 'vnw-sub-to-company'

    def __init__(self, test=None, *args, **kwargs):
        super(VnwCrawlerSubCompanySpider).__init__(*args, **kwargs)
        self.test = test
        if test:
            self.start_urls = [
                CompanySubUrlItem(
                    _id= "cong-ty-tnhh-duoc-pham-hisamitsu-viet-nam-c143979",
                    name= "Công Ty TNHH Dược Phẩm Hisamitsu Việt Nam",
                    url= "https://www.vietnamworks.com/nha-tuyen-dung/cong-ty-tnhh-duoc-pham-hisamitsu-viet-nam-c143979"
                )
            ]
            self.logger.info("Testing")
        else:
            self.create_connection()
            self.collection_company_sub_url = self.db[settings.get('MONGO_COLLECTION_COMPANY_SUB_URL')]

    def start_requests(self):
        if self.test:
            for company_url in self.start_urls:
                yield Request(company_url.url, cb_kwargs=dict(company=company_url))
        else:
            for company_url in self.collection_company_sub_url.find({}):
                company = from_dict(data_class=CompanySubUrlItem, data= company_url)
                yield Request(company_url['url'], cb_kwargs=dict(company=company))
        
    def parse(self, response, company):
        header = response.css(".hSyJBS")
        follow = header.css("p.nVini::text").get()

        about = response.css(".lhIxQn")
        items = about.css("ul.hlxyQq")
        headquarters = ""
        address = ""
        scale = ""
        career = ""
        contact = ""
        for item in items.css("li.EtJUQ"):
            p = item.css("p.type::text").get()
            if p == "Trụ sở chính":
                headquarters = item.css(".text::text").get()
            if p == "Địa chỉ":
                address = item.css(".text::text").get()
            
            if p == "Quy mô":
                scale = item.css(".text::text").get()

            if p == "Ngành nghề":
                career = item.css(".text::text").get()

            if p == "Liên hệ":
                contact = item.css(".text::text").get()
           

        offer =  []
        benefits = response.css(".fHQQTu")
        for item in benefits.css(".eAcWiq"):
            benefit = item.css(".doDYzT::text").get()
            offer.append(benefit)

        yield CompanySubDetailItem(
            _id = company._id,
            name= company.name,
            follower= follow,
            address= address,
            career= career,
            headquarters= headquarters,
            scale= scale,
            contact= contact,
            benefit=offer
        )
            