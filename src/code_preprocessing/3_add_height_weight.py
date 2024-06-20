import pandas as pd
import numpy as np
import warnings
from unidecode import unidecode
from thefuzz import fuzz
from datetime import datetime

## DECLARE CONSTANTS
SeriesKA = ["Athletics Men's 100 metres","Athletics Men's 200 metres","Athletics Men's 400 metres","Athletics Men's 800 metres","Athletics Men's 1,500 metres","Athletics Men's 5,000 metres","Athletics Men's 10,000 metres",
        "Athletics Men's Marathon","Athletics Men's 110 metres Hurdles","Athletics Men's 400 metres Hurdles","Athletics Men's 3,000 metres Steeplechase","Athletics Men's 20 kilometres Walk","Athletics Men's 50 kilometres Walk",
        "Athletics Men's High Jump","Athletics Men's Long Jump","Athletics Men's Pole Vault","Athletics Men's Triple Jump","Athletics Men's Shot Put","Athletics Men's Discus Throw","Athletics Men's Hammer Throw","Athletics Men's Javelin Throw",
        "Athletics Women's 100 metres","Athletics Women's 200 metres","Athletics Women's 400 metres","Athletics Women's 800 metres","Athletics Women's 1,500 metres","Athletics Women's 5,000 metres","Athletics Women's 10,000 metres","Athletics Women's Marathon",
        "Athletics Women's 100 metres Hurdles","Athletics Women's 400 metres Hurdles","Athletics Women's 3,000 metres Steeplechase","Athletics Women's 20 kilometres Walk","Athletics Women's High Jump","Athletics Women's Long Jump","Athletics Women's Pole Vault",
        "Athletics Women's Triple Jump","Athletics Women's Shot Put","Athletics Women's Discus Throw","Athletics Women's Hammer Throw","Athletics Women's Javelin Throw"]
SeriesWA = ["Men's 100 Metres","Men's 200 Metres","Men's 400 Metres","Men's 800 Metres","Men's 1500 Metres","Men's 5000 Metres","Men's 10,000 Metres","Men's Marathon","Men's 110 Metres Hurdles","Men's 400 Metres Hurdles","Men's 3000 Metres Steeplechase",
        "Men's 20 Kilometres Race Walk","Men's 50 Kilometres Race Walk","Men's High Jump","Men's Long Jump","Men's Pole Vault","Men's Triple Jump","Men's Shot Put","Men's Discus Throw","Men's Hammer Throw","Men's Javelin Throw","Women's 100 Metres",
        "Women's 200 Metres","Women's 400 Metres","Women's 800 Metres","Women's 1500 Metres","Women's 5000 Metres","Women's 10,000 Metres","Women's Marathon","Women's 100 Metres Hurdles","Women's 400 Metres Hurdles","Women's 3000 Metres Steeplechase",
        "Women's 20 Kilometres Race Walk","Women's High Jump","Women's Long Jump","Women's Pole Vault","Women's Triple Jump","Women's Shot Put","Women's Discus Throw","Women's Hammer Throw",
        "Women's Javelin Throw"]

## DECLARE FUNCTIONS

# Clean name field of kaggle dataset
# remove useless chars (comma, dot, dash, quotes from Kaggle Column "Name")
def clean_name_ka(nom):
    nom=nom.replace(",","")
    nom=nom.replace("-"," ")
    nom=nom.replace(".","")
    tab=nom.split(" ")
    new_tab=[]
    for i in tab:
        if((i.find('(')==-1)&(i.find(')')==-1)&(i.find('"')==-1)):
            new_tab.append(i)
    new_nom = "".join(j+" " for j in new_tab)
    new_nom = new_nom.replace('"',"")
    new_nom = unidecode(new_nom)
    return new_nom[:-1].upper()

# Clean name filled of World Athletics dataset
# remove useless chars (dot, dash from World Athletics Column "Name")
def clean_name_wa(nom):
    new_nom = unidecode(nom)
    new_nom = new_nom.replace("-"," ")
    new_nom = new_nom.replace(".","")
    return new_nom.upper()

# Matching with fuzz 
def moulinette(A,B,pct,fuzzarg):
    # A = World Athletics uniques dataset
    # B = Kaggle uniques dataset
    # pct = threshold score for fuzz
    # fuzzarg = comparaison algorythme type (1=ratio/2=partial_ration/3=token_sort_ration/4=token_set_ration/5=partial_token_sort_ration)
    listA=[] # output world athletics Name
    listB=[] # ouput kaggle Name
    listS=[] # output score fuzz
    listC=[] # output country
    listE=[] # output event
    listW=[] # output weight
    listH=[] # output height
    # Main loop in uniques World Athletics Athlete Names
    for idx,el in enumerate(A.Name):
        # get nationality/event/gender/year values
        var_noc=A.iloc[idx]['nationality']
        var_event=A.iloc[idx]['event']
        var_gender=A.iloc[idx]['gender']
        var_year=A.iloc[idx]['year']
        # build filter of Kaggle values with same NOC code, event, Sex and Year
        dfbtmp=B.loc[(B['NOC']==var_noc)&(B['Event']==var_event)&(B['Sex']==var_gender)&(B['Year']==var_year)]
        # loop in this reduced list of Athletes in Kaggle
        for idxb,elb in enumerate(dfbtmp.Name):
            # according to fuzzarg, choice of fuzz comparaison algorythm (ratio/partial_ration/token_sort_ration/token_set_ration/partial_token_sort_ration)
            # calculate comparaison score
            if(fuzzarg==1):
                score=fuzz.ratio(el,elb)
            if(fuzzarg==2):
                score=fuzz.partial_ratio(el,elb)
            if(fuzzarg==3):
                score=fuzz.token_sort_ratio(el,elb)
            if(fuzzarg==4):
                score=fuzz.token_set_ratio(el,elb)
            if(fuzzarg==5):
                score=fuzz.partial_token_sort_ratio(el,elb)
            # if score > threshold (pct argument) then append output lists with values
            if(score>=pct):
                listA.append(el)
                listB.append(elb)
                listS.append(score)
                listC.append(var_noc)
                listE.append(var_event)
                listH.append(dfbtmp.iloc[idxb]['Height'])
                listW.append(dfbtmp.iloc[idxb]['Weight'])
    # print final results
    print("    matching filter >",pct,"% :",len(listA)," on ",len(A))
    print("    global rate matching ",round(len(listA)/len(A)*100,2),"%")
    # concatenate lists in dataframe and return final dataframe with matched Names
    data = pd.DataFrame([listA,listB,listC,listE,listH,listW])
    data = data.transpose() 
    data.columns = ['WA_names','KA_names','nationality','event','height','weight']
    return data

## MAIN

## OPEN DATASETS
dfk=pd.read_csv('data_clean/KAGGLE_final.csv')
dfwad=pd.read_csv('data/2_WA_dist.csv')
dfwat=pd.read_csv('data/2_WA_temps.csv')

## Kaggle Dataset replace events name et clean useless events
dfk=dfk.replace(to_replace=SeriesKA,value=SeriesWA)
dfk=dfk[dfk['Event'].isin(SeriesWA)]

## Kaggle & WA Dataset Name field normalisation
dfk['Name'] = dfk['Name'].apply(clean_name_ka)
dfwad['Name'] = dfwad['Name'].apply(clean_name_wa)
dfwat['Name'] = dfwat['Name'].apply(clean_name_wa)

## Extract usefull rows
OGlist=['The XXVIII Olympic Games','The XXVII Olympic Games','The XXVI Olympic Games','The XXIX Olympic Games','The XXX Olympic Games','The XXXI Olympic Games','The XXXII Olympic Games']

## Convert Race Date to datetime
dfwat['Race Date']=pd.to_datetime(dfwat['Race Date'],format="%Y-%m-%d")
dfwad['Race Date']=pd.to_datetime(dfwad['Race Date'],format="%Y-%m-%d")
aftertokyo = pd.to_datetime("2021-8-9", format="%Y-%m-%d")

## backup post tokyo marks Distance before matching
dfwad_20_24=dfwad[dfwad['Race Date']>aftertokyo]
dfwad_20_24=dfwad_20_24[dfwad_20_24['Race Type']!="Combined - Group"]

dfwad=dfwad[dfwad['Race Date']<=aftertokyo]
dfwad = dfwad[dfwad['competition_name'].isin(OGlist)] # Athlètes qui ont performé aux JO
dfwad = dfwad[dfwad['Race Type']!="Combined - Group"] # Athlètes qui ont performé en épreuve individuelle
dfwad['year']=pd.to_datetime(dfwad['Race Date']).dt.year
dfwad_mini = dfwad[['Name','nationality','event','gender','year']]
dfwad_mini = dfwad_mini.drop_duplicates()

## backup post tokyo marks Time before matching
dfwat_20_24=dfwat[dfwat['Race Date']>aftertokyo]
dfwat_20_24=dfwat_20_24[dfwat_20_24['Race Type']!="Combined - Group"]

dfwat=dfwat[dfwat['Race Date']<=aftertokyo]
dfwat = dfwat[dfwat['competition_name'].isin(OGlist)] # Athlètes qui ont performé aux JO
dfwat = dfwat[dfwat['Race Type']!="Combined - Group"] # Athlètes qui ont performé en épreuve individuelle
dfwat['year']=pd.to_datetime(dfwat['Race Date']).dt.year
dfwat_mini = dfwat[['Name','nationality','event','gender','year']]
dfwat_mini = dfwat_mini.drop_duplicates()

dfk_mini = dfk[['Name','NOC','Event','Sex','Year','Height','Weight']]
dfk_mini = dfk_mini.drop_duplicates()

## Matching test
## PASS 1
print("*** PASS 1 WA DISTANCE ***")
result_d_p1 = moulinette(dfwad_mini,dfk_mini,75,1)
print("*** PASS 1 WA TEMPS ***")
result_t_p1 = moulinette(dfwat_mini,dfk_mini,75,1)

## PASS 2
## remove matching values in datasets
warnings.simplefilter(action='ignore', category=UserWarning)
dfwad_mini=dfwad_mini[~dfwad["Name"].isin(result_d_p1['WA_names'].to_list())]
dfwat_mini=dfwat_mini[~dfwat["Name"].isin(result_t_p1['WA_names'].to_list())]
dfk_mini=dfk_mini[~dfk["Name"].isin(result_t_p1['KA_names'].to_list())]
dfk_mini=dfk_mini[~dfk["Name"].isin(result_d_p1['KA_names'].to_list())]

print("*** PASS 2 WA DISTANCE ***")
result_d_p2 = moulinette(dfwad_mini,dfk_mini,80,2)
print("*** PASS 2 WA TEMPS ***")
result_t_p2 = moulinette(dfwat_mini,dfk_mini,80,2)

## PASS 3
## remove matching values in dataset 
dfwad_mini=dfwad_mini[~dfwad["Name"].isin(result_d_p2['WA_names'].to_list())]
dfwat_mini=dfwat_mini[~dfwat["Name"].isin(result_t_p2['WA_names'].to_list())]
dfk_mini=dfk_mini[~dfk["Name"].isin(result_t_p2['KA_names'].to_list())]
dfk_mini=dfk_mini[~dfk["Name"].isin(result_d_p2['KA_names'].to_list())]

print("*** PASS 3 WA DISTANCE ***")
result_d_p3 = moulinette(dfwad_mini,dfk_mini,79,3)
print("*** PASS 3 WA TEMPS ***")
result_t_p3 = moulinette(dfwat_mini,dfk_mini,79,3)

## PASS 4
## remove matching values in dataset 
dfwad_mini=dfwad_mini[~dfwad["Name"].isin(result_d_p3['WA_names'].to_list())]
dfwat_mini=dfwat_mini[~dfwat["Name"].isin(result_t_p3['WA_names'].to_list())]
dfk_mini=dfk_mini[~dfk["Name"].isin(result_t_p3['KA_names'].to_list())]
dfk_mini=dfk_mini[~dfk["Name"].isin(result_d_p3['KA_names'].to_list())]

print("*** PASS 4 WA DISTANCE ***")
result_d_p4 = moulinette(dfwad_mini,dfk_mini,75,4)
print("*** PASS 4 WA TEMPS ***")
result_t_p4 = moulinette(dfwat_mini,dfk_mini,75,4)

## PASS 5
## remove matching values in dataset 
dfwad_mini=dfwad_mini[~dfwad["Name"].isin(result_d_p4['WA_names'].to_list())]
dfwat_mini=dfwat_mini[~dfwat["Name"].isin(result_t_p4['WA_names'].to_list())]

dfk_mini=dfk_mini[~dfk["Name"].isin(result_t_p4['KA_names'].to_list())]
dfk_mini=dfk_mini[~dfk["Name"].isin(result_d_p4['KA_names'].to_list())]

print("*** PASS 5 WA DISTANCE ***")
result_d_p5 = moulinette(dfwad_mini,dfk_mini,85,5)
print("*** PASS 5 WA TEMPS ***")
result_t_p5 = moulinette(dfwat_mini,dfk_mini,85,5)

## CONCATENATE matched values in two datasets (distance/temps)

result_d=pd.concat([result_d_p1,result_d_p2,result_d_p3,result_d_p4,result_d_p5])
result_t=pd.concat([result_t_p1,result_t_p2,result_t_p3,result_t_p4,result_t_p5])
result_d=result_d.drop_duplicates()
result_t=result_t.drop_duplicates()
result_d.reset_index()
result_t.reset_index()
result_d=result_d.drop(columns=['KA_names'])
result_t=result_t.drop(columns=['KA_names'])
result_d=result_d.rename(columns={"WA_names":"Name"})
result_t=result_t.rename(columns={"WA_names":"Name"})

## CLEAN originals datasets to keep only athletes who participed to OG (but with their all perfs)
dfwad=pd.read_csv('out/WA_dist_final.csv')
dfwat=pd.read_csv('out/WA_temps_final.csv')
dfwad['Name'] = dfwad['Name'].apply(clean_name_wa)
dfwat['Name'] = dfwat['Name'].apply(clean_name_wa)
dfwad = dfwad[dfwad['Race Type']!="Combined - Group"] 
dfwat = dfwat[dfwat['Race Type']!="Combined - Group"]

dfwad_athog = dfwad.query('competition_name in @OGlist') # Athlètes qui ont performé aux JO
dfwat_athog = dfwat.query('competition_name in @OGlist') # Athlètes qui ont performé aux JO

dfwad_athog=dfwad_athog[['Name','nationality','event']].drop_duplicates()
dfwat_athog=dfwat_athog[['Name','nationality','event']].drop_duplicates()

dfwad=dfwad.merge(dfwad_athog,how='right',on=['Name','nationality','event'])
dfwat=dfwat.merge(dfwat_athog,how='right',on=['Name','nationality','event'])

## MERGE height/weight columns in cleaned datasets
dfwad=dfwad.merge(result_d,how='left', on=['Name','nationality','event'])
dfwat=dfwat.merge(result_t,how='left', on=['Name','nationality','event'])

## CONCATENATE post Tokyo marks with matching result datasets
dfwad_20_24['height']=0
dfwat_20_24['weight']=0

dfwad=pd.concat([dfwad,dfwad_20_24])
dfwat=pd.concat([dfwat,dfwat_20_24])

dfwad=dfwad.drop_duplicates()
dfwat=dfwat.drop_duplicates()

## REPLACE NAN/ZERO VALUES
list_dist_events = dfwad['event'].unique()
list_time_events = dfwat['event'].unique()

def zero_replace(df,events,field):
    for i in events:
        median_value = df.loc[(df['event']==i)&(df[field]!=0)][field].median()
        df[field] = np.where((df['event']==i)&(df[field]==0),median_value,df[field])
    return 0

dfwat['height']=dfwat['height'].fillna(0)
dfwat['weight']=dfwat['weight'].fillna(0)
dfwad['height']=dfwad['height'].fillna(0)
dfwad['weight']=dfwad['weight'].fillna(0)
zero_replace(dfwat,list_time_events,"height")
zero_replace(dfwat,list_time_events,"weight")
zero_replace(dfwad,list_dist_events,"height")
zero_replace(dfwad,list_dist_events,"weight")

## SAVE
dfwat=dfwat.reset_index(drop=True)
dfwad=dfwad.reset_index(drop=True)
dfwad.to_csv("data/3_WA_dist.csv",index=False)
dfwat.to_csv("data/3_WA_temps.csv",index=False)