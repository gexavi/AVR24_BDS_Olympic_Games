## LINEAR REGRESSION MODELING / OG PROJET / FINAL PREDICTION
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from category_encoders.leave_one_out import LeaveOneOutEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error, r2_score,median_absolute_error
from math import sqrt
from sklearn.linear_model import Lasso

## OPENING DATASETS
df=pd.read_csv('in/WA_dist_enrichie_14062024.csv')
dfv=pd.read_csv('in/WA_dist_validate_24062024_v2.csv')
dfv=dfv[['competition_name','event','rtype','rdate','name','gender','nationality','age','annual_perf_nb','annual_perf_max','annual_perf_moy','height','weight','or_perf']]

## FIELDS CHOICE
df=df.sort_values(by=['rdate'],ascending=True)
df=df.reset_index()
df=df.drop(columns=['index'])
y=df['mark']
X=df.drop(columns=['mark'])

## FUNCTION MAE/MSE/RMSE SCORE
def scoring(y,y_pred):
    scores=[]
    scores.append(r2_score(y,y_pred))
    scores.append(mean_absolute_error(y,y_pred))
    scores.append(mean_squared_error(y,y_pred))
    scores.append(sqrt(mean_squared_error(y,y_pred)))
    scores.append(median_absolute_error(y,y_pred))
    return  scores

# RANDOM SPLIT
X_train, X_test, y_train, y_test = train_test_split (X,y, test_size=0.2,random_state=32)
X_validate=dfv

# BACKUP
X_train_bck=X_train
X_test_bck=X_test
y_train_bck=y_train
y_test_bck=y_test
X_validate_bck=X_validate

# REMOVE USELESS VARIABLES
# AVEC enrichissement SANS gender/wind/rtype
X_train=X_train.drop(columns=['name','rdate','competitor.id','records','or_flag','or_perf','Place','wind','gender','rtype'])
X_test=X_test.drop(columns=['name','rdate','competitor.id','records','or_flag','or_perf','Place','wind','gender','rtype'])
X_validate=X_validate.drop(columns=['name','rdate','gender','rtype','or_perf'])

X_variables=pd.DataFrame(list(X_train.columns.values))

## RACE TYPE TO NUM
X_train=X_train.replace(to_replace=['Qualification - Group','Preliminary Round - Heat','Round 1 - Heat','Extra Race - Heat','Quarterfinal - Heat','Semifinal - Heat','Final'],value=[1,2,3,4,5,6,7])
X_test=X_test.replace(to_replace=['Qualification - Group','Preliminary Round - Heat','Round 1 - Heat','Extra Race - Heat','Quarterfinal - Heat','Semifinal - Heat','Final'],value=[1,2,3,4,5,6,7])

## ENCODE STRING TO NUM
encoder=LeaveOneOutEncoder()
X_train_loo=encoder.fit_transform(X_train,y_train)
X_test_loo=encoder.transform(X_test)
X_validate_loo=encoder.transform(X_validate)

## STANDARDISATION
scaler=StandardScaler()
X_train_loo_std=scaler.fit_transform(X_train_loo)
X_test_loo_std=scaler.transform(X_test_loo)
X_validate_loo_std=scaler.transform(X_validate_loo)

X_train_loo=X_train_loo_std
X_test_loo=X_test_loo_std
X_validate_loo=X_validate_loo_std

list_scores_label=pd.Series(['Coef determination','MeanAbsoluteError','MeanSquaredError','RMeanSquaredError','MedianAbsoluteError'])

# CREATE LASSO MODEL
print("\nLASSO MODEL")
print("===========")
lasso=Lasso(alpha=0.01,tol=0.0001,max_iter=10000)
# TRAIN MODEL
lasso.fit(X_train_loo,y_train)
# PREDICT VALIDATE
y_pred_lso_validate=lasso.predict(X_validate_loo)

resultdf=pd.DataFrame.from_records(X_validate_bck)
resultdf['y_pred_lasso']=y_pred_lso_validate
#resultdf['or_flag']=np.where(resultdf['y_pred_lasso']-resultdf['or_perf']>0,1,0)

resultdf.to_csv("out/WA_distance_validate_prediction.csv")

#with pd.ExcelWriter("debug/distance_validate_result_std.xlsx") as writer:
#    resultdf.to_excel(writer,sheet_name="predictions")
