import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from urllib.parse import urljoin
from pymongo import MongoClient

conn = MongoClient('mongodb://localhost:27017')
db = conn['vnw']
collection_company_url = db['company-url']
collection_company_sub_url = db['company-sub-url']

baseUrl = "https://www.vietnamworks.com"
url = 'https://www.vietnamworks.com/danh-sach-cong-ty?keyword=c'
webdriver = webdriver.Chrome()
webdriver.get(url)
time.sleep(2)


buttons = ""
count = 0
while True:
    count = count + 1
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    buttons = webdriver.find_element(By.CSS_SELECTOR, 'button.inuuFC.clickable')
    if buttons!="":
        buttons.click()
    else:
        break
    if count == 90:
        break

time.sleep(5)
html = BeautifulSoup(webdriver.page_source, 'html.parser')
info = []

jobDivs = html.find_all("p", class_="sc-kbousE iChegL")
for div in jobDivs:
    company_ids = div.find('a')['href']
    company_url = urljoin(baseUrl, div.find('a')['href'])
    name = div.find('a').get_text()
    if "/nha-tuyen-dung/" in company_ids:
        company_id = str(company_ids).replace("/nha-tuyen-dung/", "")
        collection_company_sub_url.find_one_and_update(
            {'_id': company_id},
            {'$set':{'name': name, 'url': company_url}},
            upsert=True
        )
                    
    elif "/companies/" in company_ids:
        company_id = str(company_ids).replace("/companies/", "")
        collection_company_sub_url.update_one(
            {'_id': company_id},
            {'$set':{'name': name, 'url': company_url}},
            upsert=True
        )
    else: 
        company_id = str(company_ids).replace("/company/", "")
        collection_company_url.update_one(
            {'_id': company_id},
            {'$set':{'name': name, 'url': company_url}},
            upsert=True
        )
    print(company_id)
    print(name)
    print(company_url)
    print("======================================================")

