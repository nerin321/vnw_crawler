import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from export_base import VnwExporter

# COLUMN_ID = "id"
# COLUMN_NAME="name"
# COLUMN_AREA = "area"

exporter = VnwExporter()
query = {}

query_area_result = exporter.find_area(query)
query_career_result = exporter.find_career(query)

export_area = []
for area in query_area_result:
    area_name = area['name']
    export_area.append(area_name)   

export_career = []
for career in query_career_result:
    career_name = career['name']
    export_career.append(career_name)

def exported_area(area):
    arr = []
    month_arr = []
    for i in range(1,13):
        date_object = datetime.strptime(str(i), "%m")
        month = str(date_object.strftime("%m"))
        month_arr.append(month)
        query = {
            'area':area,
            'day_start': { '$regex': f'/{month}/', '$options': "i" }
        }
        query_result = exporter.find_job(query)
        export_list = []
        for item in query_result:
            export_list.append(item)
        if export_list:
            count = len(export_list)
        else:
            count = 0
        arr.append(count)
    # print(month_arr)
    df = pd.DataFrame({'month': month_arr, 'job': arr})
    df.plot(x='month', y='job', kind='bar')
    plt.title(f'Biểu đồ số lượt tuyển dụng theo tháng ở {area}')

    folder_path = f'img/area/{area}'
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f'bao_cao_theo_thang.png')
    plt.savefig(file_path)
    plt.close()

def exported_career(career):
    arr = []
    month_arr = []
    for i in range(1,13):
        date_object = datetime.strptime(str(i), "%m")
        month = str(date_object.strftime("%m"))
        month_arr.append(month)
        query = {
            'career':career,
            'day_start': { '$regex': f'/{month}/', '$options': "i" }
        }
        query_result = exporter.find_job(query)
        export_list = []
        for item in query_result:
            export_list.append(item)
        if export_list:
            count = len(export_list)
        else:
            count = 0
        arr.append(count)
    # print(month_arr)
    df = pd.DataFrame({'month': month_arr, 'job': arr})
    df.plot(x='month', y='job', kind='bar')
    plt.title(f'Biểu đồ số lượt tuyển dụng theo tháng trong ngành {career}')

    name = career.replace("/", "_").strip()
    folder_path = f'img/career/{name}'
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f'bao_cao_theo_thang.png')
    plt.savefig(file_path)
    plt.close()

for ar in export_area:
    exported_area(ar)

for car in export_career:
    exported_career(car)