import pandas as pd
import numpy as np

# DISTANCE chargement dataset enrichie et dataset validation + prediction
dfd=pd.read_csv('in/WA_dist_enrichie_14062024.csv')
dfdv=pd.read_csv('out/WA_distance_validate_prediction.csv')

# TEMPS chargement dataset enrichie et dataset validation + prediction
dft=pd.read_csv('in/WA_temps_enrichie_20062024.csv')
dftv=pd.read_csv('out/WA_temps_validate_prediction.csv')

# recuperation liste athlètes (suppression des doublons)
dfdv_liste=dfdv['name'].drop_duplicates().to_list()
dftv_liste=dftv['name'].drop_duplicates().to_list()

# filtre sur uniquement les athlètes qui sont dans la liste validation
dfd=dfd[dfd['name'].isin(dfdv_liste)].reset_index()
dft=dft[dft['name'].isin(dftv_liste)].reset_index()

# format date pour variable race date
dft['rdate']=pd.to_datetime(dft['rdate'],format="%Y-%m-%d")
dfd['rdate']=pd.to_datetime(dft['rdate'],format="%Y-%m-%d")

# calcul et ajout de la variable 'coef_perf'  (rapport entre le record et la performance)
dft['coef_perf']=dft.apply(lambda x: (-(x['or_perf']-x['mark'])/x['or_perf'])*100, axis=1)
dfd['coef_perf']=dfd.apply(lambda x: ((x['or_perf']-x['mark'])/x['or_perf'])*100, axis=1)

# filtre sur les performances depuis JO Tokyo
dft=dft[dft['rdate']>'2021-08-01']
dfd=dfd[dfd['rdate']>'2021-08-01']

# TEMPS groupement pour récupérer la médiane,min,max,ecart type et count des coef_perf
dftgrp=dft.groupby(['name','event']).agg({'coef_perf':['count','median','min','max','std']}).reset_index()
# TEMPS groupement pour récupérer le nombre de fois ou l'athlète bat 'virtuellement' le record olympique
dftgrpb=dft.groupby(['name','event'])['coef_perf'].apply(lambda x: (x<0).sum()).reset_index(name='orperf_count')
# TEMPS renommage colonnes premier groupement
dftgrp.columns = ['name', 'event', 'perf_number','coef_perf_median', 'coef_best_perf', 'coef_worst_perf','coef_perf_et']
# TEMPS ajout dans le premier groupement, la colonne avec le nombre de fois ou l'athlète bat 'virtuellement' le record olympique
dftgrp['orperf_count']=dftgrpb['orperf_count']
# TEMPS calcul rapport entre nombre perf qui battent le OR et nombre de perf total
dftgrp['orperf_proba1']=dftgrp['orperf_count']/dftgrp['perf_number']
# TEMPS calcul pénalitée (en fct du nombre de perf , si <= 5 on pénalise, si >5 on pénalise pas)
dftgrp['orperf_proba2']=np.where((dftgrp['perf_number']/5)<=1,dftgrp['orperf_proba1']*(dftgrp['perf_number']/5),dftgrp['orperf_proba1'])
# TEMPS calcul bonus (en fct du nombre de la médiane des coerf_perf , si mediane < 0 on applique le bonus, sinon on applique aucun bonus)
dftgrp['orperf_proba']=np.where((dftgrp['coef_perf_median'])<0,dftgrp['orperf_proba2']*(1+abs(dftgrp['coef_perf_median']/100)),dftgrp['orperf_proba2'])
# TEMPS on retire les étapes intermédiaires
dftgrp=dftgrp.drop(columns=['orperf_proba1','orperf_proba2'])
# TEMPS tri par meilleure mediane
dftgrp=dftgrp.sort_values(by=['coef_perf_median','coef_perf_et'],ascending=[True,True])
# TEMPS merge avec prediction
dftgrp=pd.merge(dftv,dftgrp,on=['name','event'])
print(dftgrp)
# TEMPS export CSV/EXCEL
dftgrp.to_excel("debug/temps_synthese.xlsx")

# DISTANCE groupement pour récupérer la médiane,min,max,ecart type et count des coef_perf
dfdgrp=dfd.groupby(['name','event']).agg({'coef_perf':['count','median','min','max','std']}).reset_index()
# DISTANCE groupement pour récupérer le nombre de fois ou l'athlète bat 'virtuellement' le record olympique
dfdgrpb=dfd.groupby(['name','event'])['coef_perf'].apply(lambda x: (x<0).sum()).reset_index(name='orperf_count')
# DISTANCE renommage colonnes premier groupement
dfdgrp.columns = ['name', 'event', 'perf_number','coef_perf_median', 'coef_best_perf', 'coef_worst_perf','coef_perf_et']
# DISTANCE ajout dans le premier groupement, la colonne avec le nombre de fois ou l'athlète bat 'virtuellement' le record olympique
dfdgrp['orperf_count']=dfdgrpb['orperf_count']
# DISTANCE calcul rapport entre nombre perf qui battent le OR et nombre de perf total
dfdgrp['orperf_proba1']=dfdgrp['orperf_count']/dfdgrp['perf_number']
# DISTANCE calcul pénalitée (en fct du nombre de perf , si <= 5 on pénalise, si >5 on pénalise pas)
dfdgrp['orperf_proba2']=np.where((dfdgrp['perf_number']/5)<=1,dfdgrp['orperf_proba1']*(dfdgrp['perf_number']/5),dfdgrp['orperf_proba1'])
# DISTANCE calcul bonus (en fct du nombre de la médiane des coerf_perf , si mediane < 0 on applique le bonus, sinon on applique aucun bonus)
dfdgrp['orperf_proba']=np.where(dfdgrp['coef_perf_median']<0,dfdgrp['orperf_proba2']*(1+abs(dfdgrp['coef_perf_median'])/100),dfdgrp['orperf_proba2'])
# DISTANCE on retire les étapes intermédiaires
dfdgrp=dfdgrp.drop(columns=['orperf_proba1','orperf_proba2'])
# DISTANCE tri par meilleure mediane
dfdgrp=dfdgrp.sort_values(by=['coef_perf_median','coef_perf_et'],ascending=[True,True])
# DISTANCE merge avec prediction
dfdgrp=pd.merge(dfdv,dfdgrp,on=['name','event'])
print(dfdgrp)
# DISTANCE export CSV/EXCEL
dfdgrp.to_excel("debug/dist_synthese.xlsx")