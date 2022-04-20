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

### 분석을 위한 지표 
- application related 3개, update related 12개
![image](https://user-images.githubusercontent.com/70933580/164172453-9a8161ce-5b90-45bb-9ddf-439be74ca238.png)
![image](https://user-images.githubusercontent.com/70933580/164172488-7592d3b8-2e84-404b-b867-91467ed181cc.png)
![image](https://user-images.githubusercontent.com/70933580/164172509-fe2f1796-27b8-47e3-a6d6-71e22f86a6bc.png)

### 수집 데이터로 지표 계산 후 클러스터링 시행
- 클러스터 수 계산을 위한 elbow 기법
```python
# elbow 기법으로 cluster 객수 찾기
def elbow(X):
    sse =[]
    for i in range(1, 15):
        km = KMeans(n_clusters=i, algorithm='auto', random_state=42)
        km.fit(X)
        sse.append(km.inertia_)
    
    plt.plot(range(1,15), sse, marker = 'o')
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.show()

elbow(cluster_data)
```
![image](https://user-images.githubusercontent.com/70933580/164174360-14a656f5-df51-411f-ad36-47e74c214597.png)

적정 클러스터 4로 설정

### Anova test를 통한 클러스터 지표 구분
- NMiC의 p-value가 0.05보다 크기 때문에 해석에서 제외
![image](https://user-images.githubusercontent.com/70933580/164175960-abb569fa-7c59-43b3-88a7-42cccff2bb76.png)

### Clustring result / Cluster-naming
- 클러스터의 지표 별 값 정리
![image](https://user-images.githubusercontent.com/70933580/164176109-760beeda-73bd-4597-bcdf-8129b5778c5f.png)

- C1: Fast & Responsible
    - 빠른 피드백 버그 수정, 안정화 작업을 함(Critical Crush, Bug Count, Stability Count)
    - 업데이트를 가장 자주 시행함(AUPW)
    - 지속적인 신기술 도입과, 관리, 보수를 시행(APMaM & APMiM)
    - 이전 업데이트와 유사한 업데이트를 자주 진행 함(Patch Similarity)
    - 주요 카테고리: News, Finance, Business, Lifestyle, Social Networking
    - 대표 어플: 알리 익스프레스, iCatcher! Podcast player, CNN
    - 일상 생활과 관련되어 있는 카테고리
    - 오류가 발생했을 경우 신속하게 대처해야 이용자들이 불편을 느끼지 않음

- C2: Young & Innovation Focused
    - 대부분 시장에 진입한지 얼마 되지 않음(Low DoM)
    - 혁신을 가장 빨리 도입함(PFM & NMaC)
    - 신 기술을 많이 자주 도입함(PMiM)
    - 주요 카테고리: Game, Education, Graphics, Books, Health Category
    - 대표 어플:The Room, ScreenKit, AutoSleep Track Sleep
    - 새로운 서비스, 기술을 적용하고 사용하고자 하는 카테고리
    - Game Graphic의 발전, 웨어러블 기기의 도입과 같은 변화로 인해 새로운 기능을 자주 도입 함!

- C3: Sustaining & Safe Improvement
    - 기존 서비스, 기능을 유지하는 기간이 김(High APMiM)
    - 마켓에 가장 오랫동안 존재함(High DoM)
    - 업데이트를 많이 하지 않음(Low AUPW)
    - 주요 카테고리: Weather, Navigation, Medical, Reference, Sports
    - 대표 어플: Dark Sky Weather, Paypal, Land Nav Assistant Gammon Applications
    - 출시 초기 서비스 질과 앱의 안정성이 중요한 카테고리 
    - 해당 카테고리에 속한 앱의 경우 급격한 변화는 소비자가 앱 사용에 있어 이질감을 느낄 수 있음

- C4: Silence & Avoiding
    - 일주일에 패치하는 횟수가 낮음(Low AUPW)
    - 버그 수정, 안정화, 신기능 추가 빈도가 낮음(Low Bug, New, Stability Count)
    - 가장 낮은 평점(Low Average Rating)
    - 유료 어플리케이션 54%, 무료 어플리케이션 46%
    - 주요 카테고리: Shopping, Developer Tools, Utilities
    - 대표 어플: Barcode Scanner, OpenTerm, iAmNotiFied
    - 해당 카테고리에 속한 앱의 경우 시장 상황 업데이트나, 기술 업데이트가 중요 함
    - 다른 클러스터에 비해 유로 어플리케이션의 비중이 높음에도 업데이트가 미비 함


