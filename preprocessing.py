# -*- coding: utf-8 -*-
"""
Created on Mon May 10 14:37:40 2021

@author: young
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


path_dir = './master'
file_list = os.listdir(path_dir)


for a in file_list:
    sample = pd.read_excel('./master/'+a, names= ['name', 'description', 'version', 'release_date', 'release_note'],
                           header = None, sheet_name = None)
    name= []
    description = []    
    date=[]
    release_date= []
    patch_count=[]
    dom=[]
    first_major_change=[]
    for i in sample:
        name.append(sample[i].name) #이름 추가
        description.append(sample[i].description.dropna()) #디스크립션
        date.append(sample[i].release_date.dropna()) #데이트 수정
        
        ############날짜 형식 수정 ##########
        for j in date:
            date1=[]
            date1.append(j)
            date1 = pd.DataFrame(date1[0])
            date1.astype(str)
            date2 = date1['release_date'].str.split('/').apply(lambda x: pd.Series(x))
            date2[2] = date2[2].astype(str)
            date2[2] = '20'+date2[2]
                
        release_date.append(date2[2]+'-'+date2[0]+'-'+date2[1])
        release_date = pd.DataFrame(release_date)
        sample[i].release_date = release_date.T
        
        patch_count.append(len(sample[i].version.dropna()))
  
####################Duration On Market##############
        time1 = datetime.strptime(sample[i].release_date[-1:].values[0], '%Y-%m-%d')
        time2 = datetime.now()
        dom.append(int(((time2-time1).days)/7))

####################FMC#################
  
    spversion = sample[i].version.astype(str).str.split('.').apply(lambda x : pd.Series(x))

    try:
        spversion.drop(3, axis=1, inplace=True)
        spversion.drop(4, axis=1, inplace=True)
        spversion.drop(5, axis=1, inplace=True)
        spversion.drop(6, axis=1, inplace=True)
    except KeyError:
        pass    
    try:
        spversion.columns =["major", "minor", "patch"]
    except ValueError:
        spversion.columns =["major", "minor"]
        spversion.loc[:, ['minor']]=0
        spversion.loc[:, ["patch"]]=0
     
    
    sample2=pd.concat([sample[i], spversion], axis = 1)
    sample2 = sample2[['name', 'description', 'version', 'major', 'minor', 'patch', 'release_date', 'release_note']]          
    
    try:
        
        first = sample2['major'] == str(int(sample2.major.iloc[-1])+1)
        first_major = sample2[first]
    
        time1 = datetime.strptime(first_major.release_date.iloc[-1], '%Y-%m-%d')
        time2 = datetime.strptime(sample2.release_date.iloc[-1], '%Y-%m-%d')
        first_major_change.append(int(((time1-time2).days)))
    except Exception:
        first_major_change.append(0)


################## NMaC, NMiC, NPC #####################
#####criteria list
    NMaC=[]
    NMiC =[]
    NPC=[]    
    APMaM = []        
    APMiM =[]
    APPM = []
    CC=[]
##########sublist########    
    major_maintenance=[]
    count=[]
    count1=[]
    gap =[]
    
    
    sample2.dropna(subset =['version'], inplace=True)  
    sample2['minor'].fillna(0, inplace=True)
    sample2['patch'].fillna(0, inplace=True)
    major = sample2.major.unique()

    NMaC.append(major[0])
   

    
    for i in major:
        date = sample2['major'] == str(i)
        major_version = sample2[date]
        count.append(int(major_version.minor.unique()[0]))
        patch_version = major_version[major_version['patch'] !=0]
        count1.append(int(len(patch_version)))
        
        #######APMaM calculating######
        time1 = datetime.strptime(major_version.release_date.iloc[0], '%Y-%m-%d')
        time2 = datetime.strptime(major_version.release_date.iloc[-1], '%Y-%m-%d')
        major_maintenance.append(int(((time1-time2).days)))  
        
        ########APMiM calculating#######
        minor_version=major_version.drop_duplicates(['minor'], keep='last')
        minor_date = minor_version["release_date"].tolist()
        last=len(minor_version)-1        
        for k in range(0, last):            
            l = k+1
            time1 = datetime.strptime(minor_date[k], '%Y-%m-%d')
            time2 = datetime.strptime(minor_date[l], '%Y-%m-%d')
            gap.append(int(((time1-time2).days)))
    try:
        APMiM.append(statistics.mean(gap))
    except Exception:
        time1 = datetime.strptime(sample.release_date.iloc[0], '%Y-%m-%d')
        time2 = datetime.strptime(sample.release_date.iloc[-1], '%Y-%m-%d')
        APMiM.append(int(((time1-time2).days)))
        
####################APPM calculating##########

    last = len(sample2['release_date'])-1
    gap=[]
    for i in range(0, last):
        k = i+1
        time1 = datetime.strptime(sample.release_date.iloc[i], '%Y-%m-%d')
        time2 = datetime.strptime(sample.release_date.iloc[k], '%Y-%m-%d')
        gap.append(int(((time1-time2).days)))
    df = pd.DataFrame(gap)    
    try:
        APPM.append(statistics.mean(gap))
    except Exception:
         time1 = datetime.strptime(sample.release_date.iloc[0], '%Y-%m-%d')
         time2 = datetime.now()
         APPM.append(int(((time2-time1).days)))            

###############Critical Crush calcurating##########         
    try:
        Q1 = np.percentile(df.iloc[:,0], 25)
        Q3 = np.percentile(df.iloc[:,0], 75)
        IQR = Q3-Q1
        outlier_step = 1.5*IQR
        outlier_list_col = df[(df.iloc[:, 0]<Q1-outlier_step)|(df.iloc[:,0] > Q3+outlier_step)].index
        CC.append(len(outlier_list_col))
    except IndexError:
        CC.append(0)    
        
    APMaM.append(statistics.mean(major_maintenance))  
    NMiC.append(sum(count))
    NPC.append(sum(count1))    


#########APP_Rating##########
path_dir2 = './review_data'
file_list2 = os.listdir(path_dir2)

AR=[]
for i in file_list2:
    tempt = pd.read_xlsx('./review_data'+i, index_col=0)
    AR.append(tempt['STAR'].mean())



information = pd.DataFrame({'appname' : name, 
                            'description' : description,
                            'patch_count': patch_count,
                            'DoM': market,
                            'NMaC': NMaC,
                            'NMiC': NMiC,
                            'NPC': NPC,
                            'PFM': first_major_change,
                            'APMaM':APMaM,
                            'APMiM':APMiM,
                            'APPM': APPM,
                            'CC':CC,
                            'AR':AR})

information['AUPW'] = information['patch_count']/information['DoM']

#엑셀 저장
information.to_excel('./information.xlsx')
