import pandas as pd
import numpy as np
import re
import time

## OPEN DATASETS
dft=pd.read_csv("data/5_WA_temps.csv")
dfd=pd.read_csv("data/5_WA_dist.csv")

## DECLARE FUNCTION
def clean_wind(chaine):
     return str(chaine).replace("+","")
dft['wind']=dft['wind'].replace(to_replace=['NWI','w'],value=[0,0])
dft['wind']=dft['wind'].apply(clean_wind)
dft['wind']=dft['wind'].astype(float)

## SAVE
dft.to_excel("data/6_WA_temps.csv")
dfd.to_excel("data/6_WA_dist.csv")