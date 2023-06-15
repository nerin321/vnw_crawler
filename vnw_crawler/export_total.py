import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from export_base import VnwExporter

exporter = VnwExporter()
# query = {}

# query_area_result = exporter.find_area(query)
# query_career_result = exporter.find_career(query)
# query_job = exporter.find_job(query)

def export_for_month(year):
    month_arr = []
    job = []

    for i in range(1,13):
        date_object = datetime.strptime(str(i), "%m")
        month = str(date_object.strftime("%m"))
        month_arr.append(month)
        query = {
            'day_start': { '$regex': f'/{month}/.*{year}', '$options': "i" }
        }
        query_result = exporter.find_job(query)
        export_list = []
        for item in query_result:
            export_list.append(item)
        if export_list:
            count = len(export_list)
        else:
            count = 0
        job.append(count)
    
    df = pd.DataFrame({'month': month_arr, 'job': job})
    df.plot(x='month', y='job', kind='bar')
    plt.title(f'Biểu đồ số lượt tuyển dụng theo tháng')

    folder_path = f'img/total/'
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f'bao_cao_theo_thang.png')
    plt.savefig(file_path)
    plt.close()

export_for_month("2023")