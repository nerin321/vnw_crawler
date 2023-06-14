# This spider will crawl from cate job kind --> job url and company sub url
# command:
# scrapy crawl vnw-job-url
# test crawler:
# scrapy crawl vnw-job-url -a test=True

import re
import json

from urllib.parse import urlparse
from dacite import from_dict

from scrapy import Request, FormRequest
from scrapy.selector import Selector

from vnw_crawler.items.CategoryItem import CategoryJobKindItem
from vnw_crawler.items.JobItem import JobUrlItem
from vnw_crawler.items.CompanyItem import CompanySubUrlItem
from .base_spider import VnwCrawlerBaseSpider, settings

class VnwCrawlerJobUrlSpider(VnwCrawlerBaseSpider):
    name = 'vnw-job-url'
    urls = "https://ms.vietnamworks.com/job-search/v1.0/search"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://www.vietnamworks.com",
        "Referer": "https://www.vietnamworks.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Source": "Page-Container",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\""
    }

    body = {"userId":0,"query":"","filter":[{"field":"typeWorkingId","value":"1"}],"ranges":[],"order":[],"hitsPerPage":50,"page":0,"retrieveFields":["address","benefits","jobTitle","salaryMax","isSalaryVisible","jobLevelVI","isShowLogo","salaryMin","companyLogo","userId","jobLevel","jobId","jobUrl","jobKind","lastUpdatedOn","companyId","approvedOn","isAnonymous","alias","expiredOn","industries","workingLocations","services","companyName","salary","onlineOn","simpleServices","visibilityDisplay","isShowLogoInSearch","priorityOrder","skills","profilePublishedSiteMask","jobDescription","jobRequirement"]}
    
    def __init__(self, test=None,*args, **kwargs):
        super(VnwCrawlerJobUrlSpider, self).__init__(*args, **kwargs)
        self.create_connection()
        self.collection_category_job_kind = self.db[settings.get('MONGO_COLLECTION_CATEGORY_JOB_KIND')]

    def start_requests(self):
        yield Request(
            url=self.urls,
            method='POST',
            dont_filter=True,
            headers=self.headers,
            body=json.dumps(self.body),
        )

    def parse(self, response):
        data = response.json()
        job_list = data['data']
        for job in job_list:
            ids = job['jobId']
            title = job['jobTitle']
            url = job['jobUrl']

            yield JobUrlItem(
                _id = str(ids),
                name=title,
                url=url
            )

        total_page = data['meta']['nbPages']
        current_page = self.body['page']
        if current_page < total_page:
            next_page = current_page + 1
            self.body['page'] = next_page
            yield Request(
                url=self.urls,
                method='POST',
                dont_filter=True,
                headers=self.headers,
                body=json.dumps(self.body),
            )
        
