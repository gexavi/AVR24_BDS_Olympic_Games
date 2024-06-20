import pandas as pd
import numpy as np
import re
import time

## OPEN DATASETS
dft=pd.read_csv("data/3_WA_temps.csv")
dfd=pd.read_csv("data/3_WA_dist.csv")

## DECLARE FUNCTIONS
def clean_date(str):
    temp=re.sub(' [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{9}','',str)
    temp=re.sub(' [0-9]{2}:[0-9]{2}:[0-9]{2}','',temp)
    temp=re.sub('.[0-9]{9}','',temp)
    return temp

## REMOVE DUPLICATES
dft=dft.drop_duplicates()
dfd=dfd.drop_duplicates()

## RENAME COLUMNS
ColumnNameDict={'Name':'name','Race Date':'rdate','Mark':'mark','Race Type':'rtype','Birthdate':'bdate'}
dft=dft.rename(ColumnNameDict,axis='columns')
dfd=dfd.rename(ColumnNameDict,axis='columns')

## ADD AGE COLUMN
dft['bdate']=dft['bdate'].apply(clean_date)
dfd['bdate']=dfd['bdate'].apply(clean_date)
dft['bdate']=pd.to_datetime(dft['bdate'],format="%Y-%m-%d")
dfd['bdate']=pd.to_datetime(dfd['bdate'],format="%Y-%m-%d")
dft['age'] = (dft['rdate'] - dft['bdate']) / np.timedelta64(1,'D')/365.25
dfd['age'] = (dfd['rdate'] - dfd['bdate']) / np.timedelta64(1,'D')/365.25
dft=dft.drop(columns=['bdate'])
dfd=dfd.drop(columns=['bdate'])

## SAVE
dft=dft.reset_index(drop=True)
dfd=dfd.reset_index(drop=True)
dft.to_excel("data/4_WA_temps.csv")
dfd.to_excel("data/4_WA_dist.csv")
 