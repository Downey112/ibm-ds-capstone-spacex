import sys,json,warnings;warnings.filterwarnings('ignore')
import pandas as pd,numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt,seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
d=sys.argv[1]
data=pd.read_csv(d+'/p2.csv');X=pd.read_csv(d+'/p3.csv')
Y=data['Class'].to_numpy();X=preprocessing.StandardScaler().fit(X).transform(X)
Xtr,Xte,Ytr,Yte=train_test_split(X,Y,test_size=0.2,random_state=2)
grids={'Logistic Regression':(LogisticRegression(),{'C':[0.01,0.1,1],'penalty':['l2'],'solver':['lbfgs']}),
'SVM':(SVC(),{'kernel':('linear','rbf','poly','rbf','sigmoid'),'C':np.logspace(-3,3,5),'gamma':np.logspace(-3,3,5)}),
'Decision Tree':(DecisionTreeClassifier(random_state=0),{'criterion':['gini','entropy'],'splitter':['best','random'],'max_depth':[2*n for n in range(1,10)],'max_features':['sqrt'],'min_samples_leaf':[1,2,4],'min_samples_split':[2,5,10]}),
'KNN':(KNeighborsClassifier(),{'n_neighbors':list(range(1,11)),'algorithm':['auto','ball_tree','kd_tree','brute'],'p':[1,2]})}
res={}
for n,(m,g) in grids.items():
  cv=GridSearchCV(m,g,cv=10).fit(Xtr,Ytr);yh=cv.predict(Xte)
  res[n]=dict(cv=round(cv.best_score_,4),test=round(cv.score(Xte,Yte),4),params={k:(float(v) if isinstance(v,np.floating) else v) for k,v in cv.best_params_.items()},cm=confusion_matrix(Yte,yh).tolist())
print(json.dumps(res,indent=1))
json.dump(res,open(d+'/ml.json','w'))
