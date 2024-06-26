## LINEAR REGRESSION MODELING / OG PROJET
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import zipfile
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from category_encoders.leave_one_out import LeaveOneOutEncoder
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import mean_squared_error,mean_absolute_error, r2_score,make_scorer
from math import sqrt
from sklearn.linear_model import Ridge,Lasso,LinearRegression,ElasticNet
 
## OPENING DATASETS
zf = zipfile.ZipFile('in/WA_dist_enrichie_14062024.zip') 
df = pd.read_csv(zf.open('WA_dist_enrichie_14062024.csv'))
    
## FIELDS CHOICE
df=df.sort_values(by=['rdate'],ascending=True)
df=df.reset_index()
df=df.drop(columns=['index'])
df=df[df['rdate']<"2024-01-01"]
y=df['mark']
X=df.drop(columns=['mark'])
    
# RANDOM SPLIT
X_train, X_test, y_train, y_test = train_test_split (X,y, test_size=0.2,random_state=32)

# MANUAL SPLIT 
#X_train=X[:int(len(X)*0.8)]
#y_train=y[:int(len(y)*0.8)]
#X_test=X[-int(len(X)*0.2):]
#y_test=y[-int(len(y)*0.2):]

# BACKUP
X_train_bck=X_train
X_test_bck=X_test
y_train_bck=y_train
y_test_bck=y_test

# REMOVE USELESS VARIABLES
X_train=X_train.drop(columns=['name','rdate','competitor.id','Place','records','or_flag','or_perf'])
X_test=X_test.drop(columns=['name','rdate','competitor.id','Place','records','or_flag','or_perf'])

# ENCODING CATEGORICAL VARIABLES
## GENDER TO NUM
df['gender']=df['gender'].replace(to_replace=['M','W'],value=[1,0])
## RACE TYPE TO NUM
df=df.replace(to_replace=['Qualification - Group','Preliminary Round - Heat','Round 1 - Heat','Extra Race - Heat','Quarterfinal - Heat','Semifinal - Heat','Final'],value=[1,2,3,4,5,6,7])

## ENCODE TO NUM
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

# CREATE GRIDCV multi models
class EstimatorSelectionHelper:
    def __init__(self, models, params):
        self.models = models
        self.params = params
        self.keys = models.keys()
        self.grid_searches = {}
    
    def fit(self, X, y, **grid_kwargs):
        for key in self.keys:
            print('Running GridSearchCV for %s.' % key)
            model = self.models[key]
            params = self.params[key]
            grid_search = GridSearchCV(model, params, **grid_kwargs)
            grid_search.fit(X, y)
            self.grid_searches[key] = grid_search
        print('Done.')
    
    def score_summary(self, sort_by='mean_test_score'):
        frames = []
        for name, grid_search in self.grid_searches.items():
            frame = pd.DataFrame(grid_search.cv_results_)
            frame = frame.filter(regex='^(?!.*param_).*$')
            frame['estimator'] = len(frame)*[name]
            frames.append(frame)
        df = pd.concat(frames)
        
        df = df.sort_values([sort_by], ascending=False)
        df = df.reset_index()
        #df = df.drop(['rank_test_score', 'index'], 1)
        
        columns = df.columns.tolist()
        columns.remove('estimator')
        columns = ['estimator']+columns
        df = df[columns]
        return df

models = { 
    'Linear Regression': LinearRegression(),
    'Ridge': Ridge(),
    'Lasso': Lasso(),
    'Elastic Net': ElasticNet()
}

params = { 
    'Linear Regression': {},
    'Ridge': {'alpha': [0.01,0.1,1,10],'tol': [0.0001,0.001]},
    'Lasso':  {'alpha': [0.01,0.1,1,10],'tol': [0.0001,0.001],'max_iter':[1000,10000,25000]},
    'Elastic Net': {'alpha': [0.01,0.1,1,10],'l1_ratio':np.arange(0.40,1.00,0.10),'tol': [0.0001,0.001],'max_iter':[1000,10000]}
}

helper_std = EstimatorSelectionHelper(models, params)
helper_std.fit(X_train_loo_std, y_train,scoring='neg_root_mean_squared_error', n_jobs=-1,cv=10)
result_std=helper_std.score_summary()
result_std.to_excel("debug/hyperparams_dist_std_result.xlsx")

helper_mms = EstimatorSelectionHelper(models, params)
helper_mms.fit(X_train_loo_mms, y_train,scoring='neg_root_mean_squared_error', n_jobs=-1,cv=10)
result_mms=helper_mms.score_summary()
result_mms.to_excel("debug/hyperparams_dist_mms_result.xlsx")