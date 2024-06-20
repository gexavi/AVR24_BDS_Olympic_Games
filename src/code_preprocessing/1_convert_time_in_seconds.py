import pandas as pd
import numpy as np

##### FUNCTIONS DECLARE
def time_to_s(A,column_name):
    # new series
    new_time_s=[]
    # main loop
    maxval=len(A.Mark)
    for idx,val in enumerate(A.Mark):
        # cleaning bad chars / replace h,m by : char
        val=str(val)
        val=val.replace("s","")
        val=val.replace('"',"")
        val=val.replace("h",":")
        val=val.replace("m",":")
        val=val.replace(" ","")
        if(val[-1]==':'):
            val=val[:len(val)-1]
        # split with ":" separator
        tab=val.split(":")
        # if 3 parts then calculate h*3600+m*60+s
        if(len(tab)==3):
            total=float(tab[2])+(float(tab[1])*60)+(float(tab[0])*3600)
        # if 2 parts then calculate m*60+s
        if(len(tab)==2):
            total=float(tab[1])+(float(tab[0])*60)
        # if 1 part then do nothing (string equal DNS,NM,DQ,DNF or distance mark or time mark < 60 secondes) 
        if(len(tab)==1):
            total=tab[0]
        print(f"Convert time column in seconds, row {idx}/{maxval}",end="\r")
        new_time_s.append(total)
    return pd.Series(new_time_s)

###### OPENING DATASETS   
WA_temps=pd.read_csv("data_clean/WA_temps.csv")
WA_dist=pd.read_csv("data_clean/WA_dist.csv")

###### CLEANING NAN
WA_temps = WA_temps.dropna(axis=0,how='all',subset=['Mark'])
WA_dist = WA_dist.dropna(axis=0,how='all',subset=['Mark'])

###### CONVERT TIME MARK COLUMNS IN SECONDS
WA_temps['Mark'] = time_to_s(WA_temps,'Mark')

###### SAVE
WA_temps=WA_temps.reset_index(drop=True)
WA_dist=WA_dist.reset_index(drop=True)
WA_temps.to_csv("data/1_WA_temps.csv",index=False)
WA_dist.to_csv("data/1_WA_dist.csv",index=False)