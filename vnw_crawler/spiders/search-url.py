# This spider will crawl company url
# command
# scrapy crawl vnw-search-url

import re
import scrapy

from vnw_crawler.items.CompanyItem import CompanyUrlItem, CompanySubUrlItem
from .base_spider import VnwCrawlerBaseSpider

def get_company_url():
    return f"https://{VnwCrawlerBaseSpider.domain}/danh-sach-cong-ty?keyword=c"


class VnwCrawlerCompanyUrlSpider(VnwCrawlerBaseSpider):
    name = 'vnw-search-url'
    start_urls = [get_company_url()]

    def parse(self, response):
        company_list = response.css(".kMGpzA")
        for company in company_list.css(".fIewdJ"):
            company_info = company.css(".dFvoev")
            url = company_info.xpath("a/@href").get()
            title = company_info.xpath("a/text()").get()

            if "https://www.vietnamworks.com/nha-tuyen-dung/" in url:
                company_ids = url.replace("https://www.vietnamworks.com/nha-tuyen-dung/", "")
                    
                yield CompanySubUrlItem(
                    _id = company_ids,
                    name=title,
                    url= url
                )
            elif "https://www.vietnamworks.com/companies/" in url:
                company_id = url.replace("https://www.vietnamworks.com/companies/", "")
                yield CompanySubUrlItem(
                    _id = company_id,
                    name=title,
                    url= url
                )
            else: 
                company_id = url.replace("https://www.vietnamworks.com/company/", "")
                yield CompanyUrlItem(
                    _id = company_id,
                    name=title,
                    url= url
                )