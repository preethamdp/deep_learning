import pandas as pd
import quandl
import math
import numpy as np
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = quandl.get('WIKI/GOOGL')
df.to_csv("google-stock.csv")
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume']]
df['HL_PCT'] = (df['Adj. High']-df['Adj. Close'])/df['Adj. Close']
df['PCT_change'] = (df['Adj. Close']-df['Adj. Open'])/df['Adj. Open']
df = df[['Adj. Close','HL_PCT','PCT_change','Adj. Volume']]

forecast_col = "Adj. Close"
df.fillna(-99999,inplace=True)

forecast_out = int(math.ceil(0.01*len(df)))

df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)

X = np.array(df.drop(['label'],1))
Y = np.array(df['label'])

X = preprocessing.scale(X)

X_train, X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2)

clf = LinearRegression()
clf.fit(X_train,Y_train)
accuracy = clf.score(X_test,Y_test)

print(accuracy)


