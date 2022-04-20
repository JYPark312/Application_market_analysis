# Application_market_analysis 논문 연구

## 박영준

### 연구 목적
- 어플리케이션 업데이트 기록 분석을 통한 어플리케이션 마켓 혁신 양상 분석

### Keywork
- update note, market analysis, clustering

### 데이터 수집 
- URL 크롤링
```python
driver.get('https://sensortower.com/ios/rankings/top/iphone/us/developer-tools?locale=ko&date=2021-03-31')
link_list=[]
appname=[]
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
aclass = soup.findAll('a', {'class','name'})
driver.find_element_by_css_selector('#rankings > div.shadowed-st.content.rankings-table-container.flex-span-12 > div.flex-span-12.alert-section > button').click()
time.sleep(3)
for link in aclass:
    if 'href' in link.attrs:
        link_list.append("https://sensortower.com"+link.attrs['href'])
    appname.append(link.text)
```

- 앱 정보, 패치노트 크롤링 (Sensor tower, App store)
  - 사전 작업으로 대상 어플의 sensor tower 주소와 id number로 공식 사이트 주소를 만든 후 크롤링
```python

for number in range(0, len(link_list)):
    url = link_list[number]
    driver.get(url[0])
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
    appname.append(soup.find('div', {'class','app-name-publisher'}).text.strip())#어플 이름
    description.append(soup.find('div', {'class', 'description-text collapsed'}).text.strip())#디스크립션
    table = soup.find('table', {'class', 'table'})#업데이트 버전, 날짜
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
        
    url2 = id[number]      
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
   
    
wb.save("data.xlsx")
```

