import pandas as pd
import numpy as np
import re
import time

## OPEN DATASETS
dft=pd.read_csv("data/6_WA_temps.csv")
dfd=pd.read_csv("data/6_WA_dist.csv")

## PREPARE RACE DATE
dft['rdate']=dft['rdate'].apply(clean_date)
dfd['rdate']=dfd['rdate'].apply(clean_date)
dft['rdate']=pd.to_datetime(dft['rdate'],format="%Y-%m-%d")
dfd['rdate']=pd.to_datetime(dfd['rdate'],format="%Y-%m-%d")

## DECLARE FUNCTION
def annual_perf_stat(X):
    max=len(X)
    for idx,el in enumerate(X.name):
            moyperf=0
            maxperf=0
            nbperf=0
            print("last annual perf bonus ",idx,"/",max,"               ",end="\r")
            rdate=X.iloc[idx]['rdate']
            rdatem1=rdate-pd.Timedelta(days=365)
            event=X.iloc[idx]['event']
            sampledf=X[(X.event==event)&(X.rdate<rdate)&(X.name==el)&(X.rdate>rdatem1)]
            moyperf=sampledf['mark'].mean()
            maxperf=sampledf['mark'].max()
            nbperf=len(sampledf)
            X.at[idx,'annual_perf_nb']=nbperf
            X.at[idx,'annual_perf_moy']=moyperf
            X.at[idx,'annual_perf_max']=maxperf
    return None
    
## ADDING LAST ANNUAL PERF BONUS FEATURE ( -1 year date < perfs < race date )
dft['annual_perf_nb']=0
dfd['annual_perf_nb']=0
dft['annual_perf_max']=0
dfd['annual_perf_max']=0
dft['annual_perf_moy']=0
dfd['annual_perf_moy']=0
annual_perf_stat(dft)
dft.to_csv("data/7_WA_temps.csv",index=False)
annual_perf_stat(dfd)
dfd.to_csv("data/7_WA_dist.csv",index=False)