# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from collections import defaultdict
from dataclasses import asdict
import pymongo

# import item
from vnw_crawler.items.CategoryItem import CategoryAreaItem, CategoryCareerItem, CategoryJobKindItem, CategoryRankItem
from vnw_crawler.items.CompanyItem import CompanyDetailItem, CompanySubUrlItem, CompanyUrlItem
from vnw_crawler.items.JobItem import JobUrlItem, JobDetailItem

from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class VnwCrawlerPipeline:
    def __init__(self):
        self.create_connection()
        self.count = defaultdict(int)

    def create_connection(self):
        conn=pymongo.MongoClient(
            settings.get('MONGO_HOST'),
            settings.get('MONGO_PORT')
        )

        db = conn[settings.get('MONGO_DB_NAME')]
        self.collection_company_url = db[settings['MONGO_COLLECTION_COMPANY_URL']]
        self.collection_company_sub_url = db[settings['MONGO_COLLECTION_COMPANY_SUB_URL']]
        self.collection_company_detail = db[settings['MONGO_COLLECTION_COMPANY_DETAIL']]
        self.collection_category_area = db[settings['MONGO_COLLECTION_CATEGORY_AREA']]
        self.collection_category_rank = db[settings['MONGO_COLLECTION_CATEGORY_RANK']]
        self.collection_category_job_kind = db[settings['MONGO_COLLECTION_CATEGORY_JOB_KIND']]
        self.collection_category_career = db[settings['MONGO_COLLECTION_CATEGORY_CAREER']]
        self.collection_job_url = db[settings['MONGO_COLLECTION_JOB_URL']]
        self.collection_job_detail = db[settings['MONGO_COLLECTION_JOB_DETAIL']]

    def process_item(self, item, spider):
        if hasattr(spider, "test") and spider.test:
            print("debug - db save", item)

        if isinstance(item, CategoryAreaItem):
            self.save_db(self.collection_category_area, item, "cate-area")
        elif isinstance(item, CategoryCareerItem):
            self.save_db(self.collection_category_career, item, "cate-career")
        elif isinstance(item, CategoryJobKindItem):
            self.save_db(self.collection_category_job_kind, item, "cate-job-kind")
        elif isinstance(item, CategoryRankItem):
            self.save_db(self.collection_category_rank, item, "cate-employ-rank")
        
        elif isinstance(item, CompanyUrlItem):
            self.save_db(self.collection_company_url, item, "company-url")
        elif isinstance(item, CompanySubUrlItem):
            self.save_db(self.collection_company_sub_url, item, "company-sub-url")
        elif isinstance(item, CompanyDetailItem):
            if item._id is None:
                self.save_db(self.collection_company_detail, item, "company-detail")
            else:
                self.append_set_db(self.collection_company_detail,item._id, "company-detail")
        
        elif isinstance(item, JobUrlItem):
            self.save_db(self.collection_job_url, item, "job-url")
        elif isinstance(item, JobDetailItem):
            self.save_db(self.collection_job_detail, item, "job-detail")
        return item

    def save_db(self, collection, item, kind):
        print("[DB] - Adding", kind, "#", item._id)
        try:
            collection.update_one({'_id': item._id},
                                  {"$set": asdict(item)},
                                  upsert=True)
            self.count[kind] += 1
            print("Saved:", self.count[kind], kind)
        except Exception:
            pass
    
    def append_set_db(self, collection, key, item, kind):
        it = asdict(item)
        del it["_id"]
        print("[DB] - Appending", kind, "#", key, it)
        try:
            collection.find_one_and_update(
                {'_id': key},
                {'$addToSet':it},
                upsert=True
            )
            
        except Exception as e:
            print(e)
            pass