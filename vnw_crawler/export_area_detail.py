import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from export_base import VnwExporter

exporter = VnwExporter()
query = {}

query_area_result = exporter.find_area(query)
query_career_result = exporter.find_career(query)
query_job = exporter.find_job(query)

ex_salarys = []
for document in query_job:
    item = document['salary']  # Thay "field" bằng trường dữ liệu thích hợp
    if item not in ex_salarys:
        ex_salarys.append(item)

export_area = []
for area in query_area_result:
    area_name = area['name']
    export_area.append(area_name)   

export_career = []
for career in query_career_result:
    career_name = career['name']
    export_career.append(career_name)

def exported_follow_career(area):
    arr = []
    careers = []
    for career in export_career:
        export_list = []
        query = {
            'area':area,
            'career': career
        }
        query_result = exporter.find_job(query)
        for item in query_result:
            export_list.append(item)
        if export_list:
            count = len(export_list)
        else:
            count = 0
        if count != 0:
            careers.append(career)
            arr.append(count)
    # print(month_arr)
    # df = pd.DataFrame({'Career': export_career, 'job': arr})
    plt.figure(figsize=(20, 10))
    plt.pie(arr, labels=None, autopct='')
    plt.title(f'Biểu đồ số lượt tuyển dụng theo ngành nghề ở {area}')
    plt.legend(careers, loc='lower right', ncol=2, bbox_to_anchor=(0.1, -0.1))


    folder_path = f'img/area/{area}'
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f'bao_cao_theo_nganh_nghe.png')
    plt.savefig(file_path)
    plt.close()

def export_follow_salary(area):
    arr = []
    salarys = []
    for salary in ex_salarys:
        export_list = []
        if salary != "Thương lượng":
            query = {
                'area' : area,
                'salary' : salary 
            }
            query_result = exporter.find_job(query)
            for item in query_result:
                export_list.append(item)

            if export_list:
                count = len(export_list)
            else:
                count = 0
            if count != 0:
                if count >=5:
                    salarys.append(salary)
                    arr.append(count)   
    plt.figure(figsize=(25, 10))
    plt.pie(arr, labels=None, autopct='')
    plt.title(f'Biểu đồ số lượt tuyển dụng theo mức lương ở {area}')
    plt.legend(salarys, loc='lower right', ncol=4, bbox_to_anchor=(0.1, -0.1))
    # df = pd.DataFrame({'salary': salarys, 'job': arr})
    # df.plot(x='salary', y='job', kind='bar')
    # plt.title(f'Biểu đồ số lượt tuyển dụng theo mức lương ở {area}')

    folder_path = f'img/area/{area}'
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f'bao_cao_theo_muc_luong.png')
    plt.savefig(file_path)
    plt.close()

for ar in export_area:
    exported_follow_career(ar)
    export_follow_salary(ar)