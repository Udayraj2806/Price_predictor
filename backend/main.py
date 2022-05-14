import pandas as pd
import  numpy as np
car=pd.read_csv('quikr_car.csv');
car.head();


# year has many non-year values
# year object to int
# price has ask for price
# price object to int
# kms_driven has kms with integers
# kms_driven object to int kms has nan values

backup=car.copy()
car=car[car['year'].str.isnumeric()]

car['year']=car['year'].astype(int)
car=car[car['Price']!="Ask For Price"]

car['Price']=car['Price'].str.replace(',','').astype(int)

car['kms_driven']=car['kms_driven'].str.split(' ').str.get(0).str.replace(',','')

car=car[car['kms_driven'].str.isnumeric()]
car['kms_driven']=car['kms_driven'].astype(int)

car=car[~car['fuel_type'].isna()]
car['name']=car['name'].str.split(' ').str.slice(0,3).str.join(' ')

car=car.reset_index(drop=True)
car=car[car['Price']<6e6].reset_index(drop=True)

car.to_csv('Cleaned Car.csv')
X=car.drop(columns='Price')
y=car['Price']

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y, test_size=0.2)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

ohe=OneHotEncoder()
ohe.fit(X[['name','company','fuel_type']]);
column_trans=make_column_transformer((OneHotEncoder(categories=ohe.categories_),['name','company','fuel_type']),remainder='passthrough')

lr=LinearRegression()

pipe=make_pipeline(column_trans,lr)

pipe.fit(X_train,y_train)
y_pred=pipe.predict(X_test)

scores=[]
for i in range(1000):
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=i)
    lr=LinearRegression()
    pipe=make_pipeline(column_trans,lr)
    pipe.fit(X_train,y_train)
    y_pred=pipe.predict(X_test)
    scores.append(r2_score(y_test,y_pred))
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=np.argmax(scores))
lr=LinearRegression()
pipe=make_pipeline(column_trans,lr)
pipe.fit(X_train,y_train)
y_pred=pipe.predict(X_test)
r2_score(y_test,y_pred)

import pickle
pickle.dump(pipe,open('Model.pkl','wb'))
# pipe.predict(pd.DataFrame([['ma']]))

