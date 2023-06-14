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

skills = []
for document in query_job:
    if "detail" in document:
        item = document["detail"]
        for i in item:
            skill = i['skills']
        for i in skill:
            if i not in skills:
                skills.append(i) 

export_area = []
for area in query_area_result:
    area_name = area['name']
    export_area.append(area_name)   

export_career = []
for career in query_career_result:
    career_name = career['name']
    export_career.append(career_name)

def exported_follow_area(career):
    arr = []
    areas = []
    for area in export_area:
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
            areas.append(area)
            arr.append(count)

    arr = np.where(np.array(arr) == 0, 0, arr)
    plt.figure(figsize=(20, 10))
    plt.pie(arr, labels=None, autopct='')
    plt.title(f'Biểu đồ số lượt tuyển dụng theo khu vực trong ngành {career}')
    plt.legend(areas, loc='lower right', ncol=2, bbox_to_anchor=(0.1, -0.1))

    name = career.replace("/", "_").strip()
    folder_path = f'img/career/{name}'
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f'bao_cao_theo_khu_vuc.png')
    plt.savefig(file_path)
    plt.close()

def exported_follow_skills(career):
    arr = []
    label = []
    top_skill = []
    value = []
    for skill in skills:
        export_list = []
        query = {
            'career': career,
            'detail.skills': skill
        }

        for item in exporter.find_job(query):
            export_list.append(item)
        if export_list:
            count = len(export_list)
        else:
            count = 0
        if count != 0:
            label.append(skill)
            arr.append(count)   
        for i in range(len(arr)-1):
            if arr[i] <= arr[i+1]:
                tam = arr[i]
                arr[i] = arr[i+1]
                arr[i+1] = tam
                
                tam = label[i]
                label[i] = label[i+1]
                label[i+1] = tam
    for i in range(11):             
        top_skill.append(label[i])
        value.append(arr[i])
    print(top_skill, value)
for car in export_career:
    exported_follow_area(car)
    exported_follow_skills(car)
