import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from export_base import VnwExporter
COLUMN_ID = "id"
COLUMN_NAME = "name"
COLUMN_ADDRESS = "address"
COLUMN_CAREER = "career"
COLUMN_CONTACT = "contact"
COLUMN_SCALE = "scale"
COLUMN_JOB_NAME = "job-name"
COLUMN_JOB_DAY_START = "job-day-start"
COLUMN_JOB_SALARY = "job-salary"

exporter = VnwExporter()
export_list = []
minScale = ['100','500','1.000','5.000','10.000','20.000']
for item in minScale:
    query = {'scale': {'$regex': f"{item}-"}}

    query_result = exporter.find_employer(query)
    
    for employ in query_result:
        employ_id = employ['_id']
        job_query = {'company_id': employ_id}
        job_result = exporter.find_job(job_query)
        for job in job_result:
            try:
                ele_resutl = {
                    # COLUMN_ID : employ['_id'],
                    COLUMN_NAME : employ['name'],
                    COLUMN_SCALE : employ['scale'],
                    COLUMN_ADDRESS : employ['address'],
                    COLUMN_CAREER : employ['career'],
                    COLUMN_CONTACT : employ['contact'],
                    COLUMN_JOB_NAME : job['name'],
                    COLUMN_JOB_DAY_START : job['day_start'],
                    COLUMN_JOB_SALARY : job['salary']
                }
                export_list.append(ele_resutl.copy())
            except:
                print("ERORR")

data = pd.DataFrame(export_list)

data.to_excel('company.xlsx', index=False)