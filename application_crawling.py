# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 15:18:48 2021

@author: young
"""

#패키지 설치
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
        
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException
import re
import requests as res
import time
import random
import openpyxl
import os
import xmltodict 
from urllib.request import urlopen 
import json
import datetime
from datetime import datetime



#드라이버 설정
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(5)


##URL 크롤링
category = ['books', 'business', 'developer-tools', 'education', 'entertainment', 
            'finance', 'food-drink', 'games', 'graphics-design', 'health-fieness',
            'lifestyle', 'medical', 'music', 'navigation', 'news', 'photo-video',
            'productivity', 'reference', 'social-networking', 'shopping', 'sports', 'travel', 'utilities']

for i in category:
    driver.get('https://sensortower.com/ios/rankings/top/iphone/us/'+i+'?locale=ko&date=2021-03-31')
    link_list=[]
    appname=[]
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    aclass = soup.findAll('a', {'class','name'})
    driver.find_element_by_css_selector('#rankings > div.shadowed-st.content.rankings-table-container.flex-span-12 > div.flex-span-12.alert-section > button').click()
    time.sleep(3)
    for link in aclass:
        if 'href' in link.attrs:
            link_list.append("https://sensortower.com"+link.attrs['href']) #리스트 수집
        appname.append(link.text)
    
    namedf = pd.DataFrame(appname)
    namedf = namedf.drop_duplicates() 
    namedf = namedf.drop([0,1,2,3,4,5,6,7,8]) #불필요한 데이터 추가 수집되어 제거
    
    link_listdf = pd.DataFrame(link_list) 
    link_listdf = link_listdf.drop_duplicates() 
    
    link_listdf.to_csv(i+'.csv', encoding='utf-8', index=False)

##어플 정보 크롤링

link_list = pd.DataFrame()
os.chdir('C:/Users/young/Downloads')

path_dir = './links'
file_list = os.listdir(path_dir)

for i in file_list: #링크 수집 파일 전체 불러와서 하나의 데이터 프레임으로 만들기
    link = pd.read_csv('./'+i_'.csv')
    link.columns = ['links']
    link['id'] = link.links.str.split('/').str[8] #데이터프레임에서 id 추출
    link_list = pd.concat([link_list, link]) #전체 데이터프레임 합치기


###################어플 데이터 수집###############

wb = openpyxl.Workbook()

for number in range(0, len(link_list)):
    url = link_list.links.iloc[number] #어플 업데이트 데이터는 외부 사이트에서 크롤링
    driver.get(url)
    time.sleep(2)
    appname=[]
    description=[]
    version=[]
    release_date = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        driver.find_element_by_css_selector('#overview-description > a').click()
        driver.find_element_by_css_selector('#app-versions > a').click()
    except Exception:
        pass
    appname.append(soup.find('div', {'class','app-name-publisher'}).text.strip()) #어플 이름
    description.append(soup.find('div', {'class', 'description-text collapsed'}).text.strip()) #디스크립션
    table = soup.find('table', {'class', 'table'}) #업데이트 버전, 날짜
    trs = table.find_all('tr')
    for idx, tr in enumerate(trs):
        try:
            if idx>=0:
                tds = tr.find_all('td')
                version.append(tds[0].text.strip())
                release_date.append(tds[4].text.strip())
        except IndexError:
            pass
    appname = pd.DataFrame(appname)
    description = pd.DataFrame(description)
    version = pd.DataFrame(version)
    try:
        version = version.drop([3]).reset_index(drop=True)
    except KeyError:
        pass
    release_date = pd.DataFrame(release_date)

############################패치노트는 공식사이트에서 크롤링#######################       
    url2 = link_list.id.iloc[number]      
    driver.get(url2)
    time.sleep(3)
    patch_note = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        driver.find_element_by_class_name("version-history").click()
        version_note = driver.find_elements_by_class_name("we-clamp")
        for number in version_note:
            patch_note.append(number.text) #패치노트 크롤링
    except Exception:
        pass
    try:
        patch_note = pd.DataFrame(patch_note)
        patch_note = patch_note.replace('\n', '', regex = True)
        patch_note = patch_note.drop([0])
        appinformation = pd.concat([appname, description, version, release_date, patch_note], axis =1)
        appinformation.columns=['appname','description', 'version', 'release_date', 'patch_note']
        appinformation = appinformation.replace('\n', ' ', regex = True)
    except Exception:
        pass    
    
    ws = wb.create_sheet()
    try:
        for data in appinformation.values.tolist():
            ws.append(data)
    except Exception:
        pass
 
    
wb.save("data.xlsx") #데이터 저장



