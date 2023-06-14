import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from export_base import VnwExporter

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

def exported_career(career):
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
    # print(month_arr)
    # df = pd.DataFrame({'Career': export_career, 'job': arr})
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

for car in export_career:
    exported_career(car)