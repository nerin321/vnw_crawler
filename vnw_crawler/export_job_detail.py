import sys
import pandas as pd

from export_base import VnwExporter

COLUMN_ID = "id"
COLUMN_NAME = "name"
COLUMN_AREA = "area"
COLUMN_COMPANY = "company"
COLUMN_SALARY = "salary"
COLUMN_CAREER = "career"
COLUMN_RANK = "rank"
COLUMN_DAYSTART = "day_start"

COLUMN_SKILL = "skill"
COLUMN_LANGUAGE = "language"

exporter = VnwExporter()
query={}

query_result = exporter.find_job(query)
exported_list = []

for job in query_result:
    try:
        ele_result = {
            COLUMN_ID: job['_id'],
            COLUMN_NAME: job['name'],
            COLUMN_AREA: job['area'],
            COLUMN_COMPANY: job['company'],
            COLUMN_DAYSTART: job['day_start'],
            COLUMN_SALARY: job['salary'],
            COLUMN_RANK: job['rank'],
        }
        # detail = job['detail']
        for item in job['career']:
            ele_result[COLUMN_CAREER] = item
            exported_list.append(ele_result.copy())
        for item in job['detail']:
            ele_result[COLUMN_LANGUAGE] = item['language']
            for skill in item['skills']:
                ele_result[COLUMN_SKILL]=skill
        
                exported_list.append(ele_result.copy())
    except:
        print("error")

data=pd.DataFrame(exported_list)
data.to_excel(f"job-detail.xlsx", index=False)
