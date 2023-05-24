# This spider will crawl job url --> job detail
# command:
# scrapy crawl vnw-job-detail
# scrapy crawl vnw-job-detail -a test=True

import re

from dacite import from_dict
from scrapy import Request

from vnw_crawler.items.JobItem import JobUrlItem, JobDetailItem
from vnw_crawler.items.CompanyItem import CompanySubUrlItem, CompanyUrlItem
from .base_spider import VnwCrawlerBaseSpider, settings

class VnwCrawlerJobUrlSpider(VnwCrawlerBaseSpider):
    name = 'vnw-job-detail'

    def __init__(self, test=None,*args, **kwargs):
        super(VnwCrawlerJobUrlSpider, self).__init__(*args, **kwargs)
        self.test = test
        if test:
            self.start_urls = [
                JobUrlItem(
                    _id= "1650027",
                    name= "[Tuyển Gấp] Nhân Viên Biên Phiên Dịch Tiếng Nhật/ Japanese Interpreter",
                    date_update= "2023-05-17T15:12:20+07:00",
                    url= "https://www.vietnamworks.com/tuyen-gap-nhan-vien-bien-phien-dich-tieng-nhat-japanese-interpreter-1650027-jv"
                )
            ]
            self.logger.info("Testing")
        else:
            self.create_connection()
            self.collection_job_url = self.db[settings.get('MONGO_COLLECTION_JOB_URL')]

    def start_requests(self):
        if self.test:
            for job_url in self.start_urls:
                yield Request(job_url.url, cb_kwargs=dict(job_url=job_url))
        else:
            for job_url in self.collection_job_url.find({}):
                job = from_dict(data_class=JobUrlItem, data=job_url)
                yield Request(job_url['url'], cb_kwargs=dict(job_url=job))

    def parse(self, response, job_url):
        # job_detail = JobDetailItem(
        #     _id = job_url._id,
        #     name= job_url.name,
        #     # job_kind=job_url.job_kind,
        #     detail=[]
        # )
        detail = []

        page_foreground = response.css(".page-job-detail__header ")
        job_header =page_foreground.css(".job-header-info")
        for item in job_header:
            urgent_label = item.xpath("span/text()").get()
            if urgent_label:
                urgent = urgent_label
            else:
                urgent = ""
            
            sub_company = item.css(".company-name")
            compamy_name = sub_company.xpath("a/span/text()").get()
            company_sub_url = sub_company.xpath("a/@href").get()
            if "https://www.vietnamworks.com/nha-tuyen-dung/" in company_sub_url:
                company_id = company_sub_url.replace("https://www.vietnamworks.com/nha-tuyen-dung/", "")
                yield CompanySubUrlItem(
                    _id = company_id,
                    name=compamy_name,
                    url= company_sub_url
                )
            elif "https://www.vietnamworks.com/companies/" in company_sub_url:
                company_id = company_sub_url.replace("https://www.vietnamworks.com/companies/", "")
                yield CompanySubUrlItem(
                    _id = company_id,
                    name=compamy_name,
                    url= company_sub_url
                )
            else: 
                company_id = company_sub_url.replace("https://www.vietnamworks.com/company/", "")
                yield CompanyUrlItem(
                    _id = company_id,
                    name=compamy_name,
                    url= company_sub_url
                )
            

            location = item.css(".company-location")
            area = location.xpath("a/text()").get()

            salary = item.css(".salary strong::text").get()

            text = item.css("span.expiry::text").get()
            day_left = text.strip()
            # day_left = int(''.join(filter(str.isdigit, day_left_text)))
        day_start = ""
        rank = ""
        skills = ""
        lang = ""
        page_job_detail = response.css(".page-job-detail__detail")
        job_info = page_job_detail.css(".box-summary")
        for items in job_info.css(".summary-item"):
            content_label = items.css(".content-label::text").get()
            content = items.css(".content::text").get()
            if content_label == "Ngày Đăng Tuyển":
                day_start = content.strip()
            elif content_label == "Cấp Bậc":
                rank = content.strip()
            elif content_label == "Ngành Nghề":
                caree = []
                item = items.css(".content")
                for a in item.css("a"):
                    ca = a.css("a::text").get()
                    caree.append(ca)
            elif content_label == "Kỹ Năng":
                skills = content.strip()
            elif content_label == "Ngôn Ngữ Trình Bày Hồ Sơ":
                lang = content.strip()
        
        offer = []
        key_word = []

        offers = page_job_detail.css(".what-we-offer")
        for items in offers.css(".benefit"):
            contents = items.css("div.benefit-name::text").get()
            content=contents.strip()
            offer.append(content)
        
        description=""
        job_description = page_job_detail.css(".job-description")
        description = job_description.css(".description::text").getall()
        description = [s.strip() for s in description if s.strip()]

        job_requirements=""
        job_requirements = page_job_detail.css(".job-requirements")
        requirement = job_requirements.css(".requirements::text").getall()
        requirement = [s.strip() for s in requirement if s.strip()]

        location=""
        job_location = page_job_detail.css(".job-locations")
        location = job_location.css(".location-name::text").get()
        if location:
            adress = location.strip()
        else:
            adress = ""

        job_tag = page_job_detail.css(".job-tags")
        for tags in job_tag.css("a"):
            tag = tags.css("span.tag-name::text").get()
            key_word.append(tag) 
        detail.append({
            "offers" : offer,
            "day _start" : day_start,
            "skills" : skills,
            "language" : lang,
            "description" : description,
            "requirements" : requirement,
            "adress" : adress,
            "tag" : key_word,
        })

        yield JobDetailItem(
            _id = job_url._id,
            name= job_url.name,
            company=compamy_name,
            area=area,
            salary=salary,
            date_update=job_url.date_update,
            day_left=day_left,
            rank=rank,
            urgent=urgent,
            career=caree,
            detail=detail
        )