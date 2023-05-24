# This spider will crawl company url
# command
# scrapy crawl vnw-company-url

import re
import scrapy

from vnw_crawler.items.CompanyItem import CompanyUrlItem
from .base_spider import VnwCrawlerBaseSpider

def get_company_url():
    return f"https://{VnwCrawlerBaseSpider.domain}/danh-sach-cong-ty"

class VnwCrawlerCompanyUrlSpider(VnwCrawlerBaseSpider):
    name = 'vnw-company-url'
    start_urls = [get_company_url()]

    def parse(self, response):
        company_list = response.css(".eyXHBE")
        for company in company_list.css(".forjik"):
            company_info = company.css(".ZULDB")
            url = company_info.xpath("a/@href").get()
            title = company_info.xpath("a/text()").get()

            yield CompanyUrlItem(
                _id = url.replace("/company/", ""),
                name= title,
                url= self.join_url(url)
            )
        
        # next_button = response.css('button.eYidrh')
        # if next_button:
        #     yield scrapy.Request(response.url, callback=self.parse)
