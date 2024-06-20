import pandas as pd
import numpy as np

## DECLARE CONSTANTS
WA_distlist = ["Men's High Jump","Men's Long Jump","Men's Pole Vault","Men's Triple Jump","Men's Shot Put","Men's Discus Throw","Men's Hammer Throw","Men's Javelin Throw","Women's High Jump","Women's Long Jump","Women's Pole Vault",
        "Women's Triple Jump","Women's Shot Put","Women's Discus Throw","Women's Hammer Throw","Women's Javelin Throw"]
WA_timelist = ["Men's 100 Metres","Men's 200 Metres","Men's 400 Metres","Men's 800 Metres","Men's 1500 Metres","Men's 5000 Metres","Men's 10,000 Metres","Men's Marathon","Men's 110 Metres Hurdles","Men's 400 Metres Hurdles",
        "Men's 3000 Metres Steeplechase","Men's 20 Kilometres Race Walk","Men's 50 Kilometres Race Walk","Women's 100 Metres","Women's 200 Metres","Women's 400 Metres","Women's 800 Metres","Women's 1500 Metres","Women's 5000 Metres",
        "Women's 10,000 Metres","Women's Marathon","Women's 100 Metres Hurdles","Women's 400 Metres Hurdles","Women's 3000 Metres Steeplechase","Women's 20 Kilometres Race Walk"]

## DECLARE FUNCTIONS
def construct_or(x):
    # initialisation output list
    or_series=[]
    # main loop
    maxval=len(x.Mark)
    for idx, perf in enumerate(x.Mark):
        print(f"Add Olympic record Column, row {idx}/{maxval}",end="\r")
        # check if perf is a real mark or a tag
        if(perf!="DNS")&(perf!="DNF")&(perf!="DQ")&(perf!="NM"):
            # get event date & event name
            edate=x.iloc[idx]['Race Date']
            etype=x.iloc[idx]['event']
            # check if distance or time perf
            if (etype in WA_timelist)|(etype in WA_distlist):
                if etype in WA_distlist:
                    testval=True
                if etype in WA_timelist:
                    testval=False
                # filter or record to event, sorted inverse (newer in top) , and put df in an array
                dfor_event=dfor.loc[dfor['event']==etype].sort_values(by=['record_date'],ascending=False)
                arr=array = dfor_event[['record_date','record']].values
                # array loop to find the good olympic record that match with "race date"
                i=0
                or_val=np.nan
                while True:
                    # check size array (to avoid special case : Race Date < first olympic record date)
                    if(i<len(arr)):
                        or_val=arr[i][1]
                        i=i+1 
                        if(edate>arr[i-1][0]):
                            # if race date is newer than olympic record date
                            break
                    else:
                        # if race date is older than first valid olympic record date
                        break
                # add or perf in output list
                or_series.insert(idx,or_val)
            else:
                # add NaN in output list
                or_series.insert(idx,np.nan)
        else:
            # add NaN in output list
            or_series.insert(idx,np.nan)
    return pd.Series(or_series)

## OPEN DATASETS
WA_temps=pd.read_csv("data/1_WA_temps.csv")
WA_dist=pd.read_csv("data/1_WA_dist.csv")

## ADD OLYMPIC RECORD COLUMN
dfor=pd.read_csv("in/or_history.csv")
WA_temps['Race Date']=pd.to_datetime(WA_temps['Race Date'])
WA_dist['Race Date']=pd.to_datetime(WA_dist['Race Date'])
dfor['record_date']=pd.to_datetime(dfor['record_date'])

WA_temps['or_perf']=construct_or(WA_temps)
WA_dist['or_perf']=construct_or(WA_dist)

## SAVE
WA_temps=WA_temps.reset_index(drop=True)
WA_dist=WA_dist.reset_index(drop=True)
WA_temps.to_csv('data/2_WA_temps.csv',index=False)
WA_dist.to_csv('data/2_WA_dist.csv',index=False)
