## LINEAR REGRESSION MODELING / OG PROJET
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import zipfile
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from category_encoders.leave_one_out import LeaveOneOutEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error, r2_score,median_absolute_error
from math import sqrt
from sklearn.linear_model import Ridge,Lasso,LinearRegression,ElasticNet

## OPENING DATASETS
zf = zipfile.ZipFile('in/WA_dist_enrichie_14062024.zip') 
df = pd.read_csv(zf.open('WA_dist_enrichie_14062024.csv'))

## FIELDS CHOICE
df=df.sort_values(by=['rdate'],ascending=True)
df=df.reset_index()
df=df.drop(columns=['index'])
#df=df[df['rdate']<"2024-01-01"]
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

## FUNCTION PLOT Y/Y_PRED
def plotting(y,y_pred,model):
    plt.title(model.upper())
    plt.scatter(y_pred,y)
    plt.plot((y.min(),y.max()),(y.min(),y.max()),color='black')
    plt.show()

# RANDOM SPLIT
X_train, X_test, y_train, y_test = train_test_split (X,y, test_size=0.2,random_state=32)

# BACKUP
X_train_bck=X_train
X_test_bck=X_test
y_train_bck=y_train
y_test_bck=y_test

# REMOVE USELESS VARIABLES

# AVEC enrichissement SANS gender/wind/rtype
X_train=X_train.drop(columns=['name','rdate','competitor.id','records','or_flag','or_perf','Place','wind','gender','rtype'])
X_test=X_test.drop(columns=['name','rdate','competitor.id','records','or_flag','or_perf','Place','wind','gender','rtype'])
X_variables=pd.DataFrame(list(X_train.columns.values))

# AVEC enrichissement
#X_train=X_train.drop(columns=['name','rdate','competitor.id','records','or_flag','or_perf','Place'])
#X_test=X_test.drop(columns=['name','rdate','competitor.id','records','or_flag','or_perf','Place'])
#X_variables=pd.DataFrame(list(X_train.columns.values))

# SANS enrichissement
#X_train=X_train.drop(columns=['name','rdate','competitor.id','records','or_flag','or_perf','Place','annual_perf_max','annual_perf_moy','annual_perf_nb'])
#X_test=X_test.drop(columns=['name','rdate','competitor.id','records','or_flag','or_perf','Place','annual_perf_max','annual_perf_moy','annual_perf_nb'])
#X_variables=pd.DataFrame(list(X_train.columns.values))

# ENCODE
## GENDER TO NUM
#X_train['gender']=X_train['gender'].replace(to_replace=['M','W'],value=[1,0])
#X_test['gender']=X_test['gender'].replace(to_replace=['M','W'],value=[1,0])

## RACE TYPE TO NUM
X_train=X_train.replace(to_replace=['Qualification - Group','Preliminary Round - Heat','Round 1 - Heat','Extra Race - Heat','Quarterfinal - Heat','Semifinal - Heat','Final'],value=[1,2,3,4,5,6,7])
X_test=X_test.replace(to_replace=['Qualification - Group','Preliminary Round - Heat','Round 1 - Heat','Extra Race - Heat','Quarterfinal - Heat','Semifinal - Heat','Final'],value=[1,2,3,4,5,6,7])

## ENCODE STRING TO NUM
encoder=LeaveOneOutEncoder()
X_train_loo=encoder.fit_transform(X_train,y_train)
X_test_loo=encoder.transform(X_test)

## NORMALISATION
mms=MinMaxScaler()
X_train_loo_mms=mms.fit_transform(X_train_loo)
X_test_loo_mms=mms.transform(X_test_loo)

## STANDARDISATION
scaler=StandardScaler()
X_train_loo_std=scaler.fit_transform(X_train_loo)
X_test_loo_std=scaler.transform(X_test_loo)

X_train_loo=X_train_loo_std
X_test_loo=X_test_loo_std

list_scores_label=pd.Series(['Coef determination','MeanAbsoluteError','MeanSquaredError','RMeanSquaredError','MedianAbsoluteError'])

# CREATE LR MULTI MODEL
print("\nLINEAR REGRESSION MODEL")
print("=======================")
lr=LinearRegression()
# TRAIN MODEL
lr.fit(X_train_loo,y_train)
# PREDICT
y_pred_lr=lr.predict(X_test_loo)
coef_lr=lr.coef_
# SCORE
list_scores_lr=pd.Series(scoring(y_test,y_pred_lr))

# CREATE RIDGE MODEL
print("\nRIDGE MODEL")
print("===========")
ridge=Ridge(alpha=0.01,tol=0.001)
# TRAIN MODEL
ridge.fit(X_train_loo,y_train)
# PREDICT
y_pred_rdg=ridge.predict(X_test_loo)
coef_rdg=ridge.coef_
# SCORE
list_scores_rdg=pd.Series(scoring(y_test,y_pred_rdg))
# RESULT PLOT

# CREATE LASSO MODEL
print("\nLASSO MODEL")
print("===========")
lasso=Lasso(alpha=0.01,tol=0.0001,max_iter=10000)
# TRAIN MODEL
lasso.fit(X_train_loo,y_train)
# PREDICT
y_pred_lso=lasso.predict(X_test_loo)
coef_lso=lasso.coef_
# SCORE
list_scores_lso=pd.Series(scoring(y_test,y_pred_lso))
# RESULT PLOT

# CREATE ELASTICNET MODEL
print("\nELASTICNET MODEL")
print("================")
elastic=ElasticNet(alpha=0.01,l1_ratio=0.899999,max_iter=10000,tol=0.0001)
# TRAIN MODEL
elastic.fit(X_train_loo,y_train)
# PREDICT
y_pred_eln=elastic.predict(X_test_loo)
coef_eln=elastic.coef_
# SCORE
list_scores_eln=pd.Series(scoring(y_test,y_pred_eln))

resultdf=pd.DataFrame.from_records(X_test_bck)
resultdf['mark']=y_test_bck
resultdf['lr_mark']=y_pred_lr
resultdf['rdg_mark']=y_pred_rdg
resultdf['lso_mark']=y_pred_lso
resultdf['eln_mark']=y_pred_eln

# ERROR COLUMNS
resultdf['lr_error']=abs(resultdf['mark']-resultdf['lr_mark'])
resultdf['ratio_lr_error']=(resultdf['lr_error']/resultdf['mark'])*100
resultdf['rdg_error']=abs(resultdf['mark']-resultdf['rdg_mark'])
resultdf['ratio_rdg_error']=(resultdf['rdg_error']/resultdf['mark'])*100
resultdf['lso_error']=abs(resultdf['mark']-resultdf['lso_mark'])
resultdf['ratio_lso_error']=(resultdf['lso_error']/resultdf['mark'])*100
resultdf['eln_error']=abs(resultdf['mark']-resultdf['eln_mark'])
resultdf['ratio_eln_error']=(resultdf['eln_error']/resultdf['mark'])*100

coef_lr=pd.DataFrame(coef_lr)
coef_rdg=pd.DataFrame(coef_rdg)
coef_lso=pd.DataFrame(coef_lso)
coef_eln=pd.DataFrame(coef_eln)

coefs=pd.concat([X_variables,coef_lr,coef_rdg,coef_lso,coef_eln],axis=1)
coefs.columns=(['variables','coef_lr','coef_ridge','coef_lasso','coef_elasticnet'])

scores_mdl=pd.concat([list_scores_label,list_scores_lr,list_scores_rdg,list_scores_lso,list_scores_eln],axis=1)
scores_mdl.columns=(["Score type","Linear Regression","Ridge","Lasso","ElasticNet"])

resultdf.to_csv('debug/distancefull_result_std_predict.csv',index=False)
coefs.to_csv('debug/distancefull_result_std_coefs.csv',index=False)
scores_mdl.to_csv('debug/distancefull_result_std_scores.csv',index=False)

with pd.ExcelWriter("debug/distancefull_result_std.xlsx") as writer:
    resultdf.to_excel(writer,sheet_name="predictions")
    coefs.to_excel(writer,sheet_name="coeficients",index=False)
    scores_mdl.to_excel(writer,sheet_name="Scores",index=False)

err_hist_lr=np.abs(y_test-y_pred_lr)
err_hist_lso=np.abs(y_test-y_pred_lso)
err_hist_rdg=np.abs(y_test-y_pred_rdg)
err_hist_eln=np.abs(y_test-y_pred_eln)

fig = plt.figure()
gs = fig.add_gridspec(2, 2, hspace=0, wspace=0)
(ax1, ax2), (ax3, ax4) = gs.subplots(sharex='col', sharey='row')
fig.suptitle('Errors Distribution (x=error value, y=count)')
ax1.hist(err_hist_lr,bins=100,color="red",label="Linear Regression")
ax1.legend()
ax2.hist(err_hist_lso,bins=100,color="blue",label="Ridge")
ax2.legend()
ax3.hist(err_hist_rdg,bins=100,color="green",label="Lasso")
ax3.legend()
ax4.hist(err_hist_eln,bins=100,color="orange",label="ElasticNet")
ax4.legend()
plt.savefig("debug/distancefull_std_distrib_errors.png")