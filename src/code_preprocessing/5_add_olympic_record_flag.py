import pandas as pd
import numpy as np

## OPEN DATASETS
dft=pd.read_csv("data/4_WA_temps.csv")
dfd=pd.read_csv("data/4_WA_dist.csv")

## DELETE UNVALID MARKS
NoMarkList=['NM','DNF','DNS','NT']
dft=dft.query('Mark not in @NoMarkList')
dfd=dfd.query('Mark not in @NoMarkList')

## CONVERT DATATYPE TO FLOAT
dft['Mark']=dft['Mark'].astype(float)
dfd['Mark']=dfd['Mark'].astype(float)

## ADD OR_FLAG COLUMN
dft['or_flag']=np.where(dft['mark']-dft['or_perf']<0,1,0)
dfd['or_flag']=np.where(dfd['mark']-dfd['or_perf']>0,1,0)

## SAVE
dft=dft.reset_index(drop=True)
dfd=dfd.reset_index(drop=True)
dft.to_excel("data/5_WA_temps.csv")
dfd.to_excel("data/5_WA_dist.csv")