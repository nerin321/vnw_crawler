import pymongo

from scrapy.utils.project import get_project_settings

settings = get_project_settings()

class VnwExporter:
    def __init__(self):
        self.create_connection()
    
    def create_connection(self):
        conn = pymongo.MongoClient(
            settings.get('MONGO_HOST'),
            settings.get('MONGO_PORT')
        )

        db = conn['vnw']
        self.collection_company_url = db[settings['MONGO_COLLECTION_COMPANY_URL']]
        self.collection_company_sub_url = db[settings['MONGO_COLLECTION_COMPANY_SUB_URL']]
        self.collection_company_detail = db[settings['MONGO_COLLECTION_COMPANY_DETAIL']]
        self.collection_employer_detail = db[settings['MONGO_COLLECTION_EMPLOYER_DETAIL']]

        self.collection_category_area = db[settings['MONGO_COLLECTION_CATEGORY_AREA']]
        self.collection_category_rank = db[settings['MONGO_COLLECTION_CATEGORY_RANK']]
        self.collection_category_job_kind = db[settings['MONGO_COLLECTION_CATEGORY_JOB_KIND']]
        self.collection_category_career = db[settings['MONGO_COLLECTION_CATEGORY_CAREER']]
        
        self.collection_job_url = db[settings['MONGO_COLLECTION_JOB_URL']]
        self.collection_job_detail = db[settings['MONGO_COLLECTION_JOB_DETAIL']] 

    def find(self, collection, query):
        return collection.find(query)
    
    def find_job(self, query):
        return self.find(self.collection_job_detail, query)
    
    def find_company(self, query):
        return self.find(self.collection_company_detail, query)
    
    def find_employer(self, query):
        return self.find(self.collection_employer_detail, query)
    
    def find_area(self, query):
        return self.find(self.collection_category_area, query)
    
    def find_career(self, query):
        return self.find(self.collection_category_career, query)
    
    # def cursor_to_map(self, func, query):
    #     result_map = {}

    #     query_result = func(query)
    #     for r in query_result:
    #         result_map[r["_id"]] = r

    #     return result_map
    
    # def get_map_job(self, query):
    #     return self.cursor_to_map(self.find_job, query)
    
    # def get_map_company(self, query):
    #     return self.cursor_to_map(self.find_company, query)