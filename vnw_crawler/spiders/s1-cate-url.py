# this spider will crawl Category List -> category link
# command:
# scrapy crawl vnw-cate-url

import re

from vnw_crawler.items.CategoryItem import CategoryAreaItem, CategoryCareerItem, CategoryJobKindItem, CategoryRankItem
from .base_spider import VnwCrawlerBaseSpider

def get_cate_list_url():
    return f"https://{VnwCrawlerBaseSpider.domain}/tim-viec-lam"

class VnwCrawlerCategorySpider(VnwCrawlerBaseSpider):
    name = 'vnw-cate-url'
    start_urls = [get_cate_list_url()]

    def parse(self, response):
        print("====Start====")

        domain_url = "https://www.vietnamworks.com/"

        box_left = response.css(".boxLeft")
        box_right = response.css(".boxRight")

        # extract box left
        for box in box_left.css(".box"):
            box_title = box.xpath("h5/text()").get()
            box_content = box.css(".boxContent")
            for li in box_content.css("li"):
                url = li.xpath("a/@href").get()
                title = li.xpath("a/text()").get()

                if box_title == "Tìm việc theo Ngành Nghề":
                    yield CategoryCareerItem(
                        _id = url.replace(domain_url, ""),
                        name=title,
                        url=url
                    )
                elif box_title == "Tìm việc theo Loại Hình Công Việc":
                    yield CategoryJobKindItem(
                        _id = url.replace(domain_url, ""),
                        name=title,
                        url=url
                    )
        
        # extract box right
        for box in box_right.css(".box"):
            box_title = box.xpath("h5/text()").get()
            box_content = box.css(".boxContent")
            for li in box_content.css("li"):
                url = li.xpath("a/@href").get()
                title = li.xpath("a/text()").get()

                if box_title == "Việc làm theo Khu Vực/Địa Điểm":
                    yield CategoryAreaItem(
                        _id = url.replace(domain_url, ""),
                        name=title,
                        url=url
                    )
                elif box_title == "Tìm việc theo Cấp Bậc":
                    yield CategoryRankItem(
                        _id = url.replace(domain_url, ""),
                        name=title,
                        url=url
                    )
