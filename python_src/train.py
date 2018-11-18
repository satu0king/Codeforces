
# coding: utf-8

# # Rating and Rank Predictor
# 
# - Rating is a number given to each user based on how they perform in recent contests. This is a regression problem. We used linear regression, XGboost and random forest.
# - Rank is a class given to each user like "Grand Master", "Expert", "Pupil" etc. This is a classification problem. We used logistic regression, XGboost and random forest.

# In[1]:


import pandas as pd, numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from xgboost import XGBRegressor,XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression


# In[2]:


data = pd.read_csv('../data/final.csv')


# In[3]:


data.describe()


# In[4]:


data.head()


# In[5]:


class Predictor:
    def __init__(self,data):
        self.data=data
        
        # One hot encoding or organization data
        self.data = pd.concat([self.data, pd.get_dummies(self.data["organization"],prefix='organization')], axis = 1)
        self.data.drop(["organization"], axis = 1, inplace = True)
        
        self.data = shuffle(self.data) # Shuffling data
        
        # Selecting features
        data_columns = list(self.data.columns)
        data_columns.remove("rating") # We want to predict this!
        data_columns.remove("country") # Because we are working only with Indian users 
        data_columns.remove("handle") # Identifier
        data_columns.remove("max_rating") # We want to predict this!
        data_columns.remove("rank") # We want to predict this!
        
        train, test = train_test_split(self.data, test_size = 0.3)
        
        self.x_train = train[data_columns]
        self.x_test = test[data_columns]
        
        self.y_train_rating = train["max_rating"]
        self.y_test_rating = test["max_rating"]
        self.y_train_rank = train["rank"]
        self.y_test_rank = test["rank"]
    
    def predictRatings(self):
        
        print("Rating Predictions (Rating)")
        
        self._linearRegressorRating()
        self._XGBRating()
        self._RandomForestRegressorRating()
    
    def predictRanks(self):
        print("Rank Predictions (Classification)")
        
        self._logisticRegressorRank()
        self._XGBRank()
        self._RandomForestClassifierRank()
        
    
    def _linearRegressorRating(self):
        print("<-- Linear Regression Rating Predictor -->") 
        m = LinearRegression().fit(self.x_train, self.y_train_rating)
        predictions = m.predict(self.x_test).reshape(-1, 1)
        print("R2 Score:",m.score(self.x_test, self.y_test_rating))
        print("RMS Error:",mean_squared_error(predictions,self.y_test_rating)**0.5)
        print()
    
    def _logisticRegressorRank(self):
        print("<-- Logistic Regression Rank Predictor -->") 
        m = LogisticRegression(C=5.5,max_iter=1000).fit(self.x_test, self.y_test_rank)
        predictions = m.predict(self.x_test).reshape(-1, 1)
        print("Mean Accuracy:",m.score(self.x_test, self.y_test_rank))
        print()
    
    def _RandomForestClassifierRank(self):
        print("<-- Random Forest Rank Predictor -->") 
        m = RandomForestClassifier(n_estimators = 1200, min_samples_leaf = 6, n_jobs = -1, verbose = 0).fit(self.x_train, self.y_train_rank)
        predictions = m.predict(self.x_test).reshape(-1, 1)
        print("Mean Accuracy:",m.score(self.x_test, self.y_test_rank))
        print()
    
    def _RandomForestRegressorRating(self):
        print("<-- Random Forest Rating Predictor -->") 
        m = RandomForestRegressor(n_estimators = 1200, min_samples_leaf = 6, n_jobs = -1, verbose = 0).fit(self.x_train, self.y_train_rating)
        predictions = m.predict(self.x_test).reshape(-1, 1)
        print("R2 Score:",m.score(self.x_test, self.y_test_rating))
        print("RMS Error:",mean_squared_error(predictions,self.y_test_rating)**0.5)
        print()
    
    def _XGBRating(self):
        print("<-- XG Boost Rating Predictor -->") 
        m = XGBRegressor(n_estimators=200).fit(self.x_train, self.y_train_rating)
        predictions = m.predict(self.x_test).reshape(-1, 1)
        print("R2 Score:",r2_score(self.y_test_rating,predictions))
        print("RMS Error:",mean_squared_error(predictions,self.y_test_rating)**0.5)
        print()
    
    def _XGBRank(self):
        print("<-- XG Boost Rank Predictor -->") 
        m = XGBClassifier(n_estimators=200).fit(self.x_train, self.y_train_rank)
        predictions = m.predict(self.x_test).reshape(-1, 1)
        print("Mean Score:",accuracy_score(self.y_test_rank,predictions))
        print()
        
        


# In[6]:


model = Predictor(data)

model.predictRatings()
model.predictRanks()

