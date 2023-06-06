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
                    _id = "DientuDongYangHP",
                    name= "Công Ty TNHH Điện Tử Dong Yang Hải Phòng",
                    url= "https://www.vietnamworks.com/company/DientuDongYangHP"
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
            follower = follow.strip().replace("(", "").replace(")", "")
        
        address = []
        container = response.css(".cp_container_section")
        uls = container.css("ul.cp_our_office")
        cp_address = uls.css("li div.cp_address-container")
        for item in cp_address.css("div"):
            div_text = item.css("div::text").get()
            span_text = item.css("span::text").get()
            
            if div_text is not None:
                div_content = div_text.strip()
            else:
                div_content = ""
            if span_text is not None:
                span_content = span_text.strip()
            else:
                span_content = ""

            if div_content != "":
                address.append(div_content)
            elif span_content != "":
                address.append(span_content)
        for item in cp_address.css("p"):
            p = item.css("p::text").get()
            b = item.css("b::text").get()

            if p is not None:
                p_content = p.strip()
            else:
                p_content = ""
            if b is not None:
                b_content = b.strip()
            else:
                b_content = ""
            
            if p_content != "":
                address.append(p_content)
            elif b_content != "":
                address.append(b_content)
        for li in cp_address.css("ul li"):
            content=li.css("li::text").get()
            if content is not None:
                text=content.strip()
            if text != "":
                address.append(text)   
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
                    
        