# Getting HMM parameters from data
import sklearn.metrics
from rftest import *
import sys
import pandas as pd
from hmm import *
from window import *
import pickle
# filelist=sys.argv[1]
# ntree=sys.argv[2]
# if len(sys.argv)==4:
  # kick=sys.argv[3]
# else:
  # kick=""
# ntree=int(ntree)
# filelist='test.txt'
def trainpara(filelist,kick="",ntree=100):
  Xcombined=""
  ycombined=""
  xlist=[]
  ylist=[]
  with open(filelist,'r') as f:
    for line in f: #exp "MATA00-1000796-20210610-170838\n"
      id=line.rstrip() # exp "MATA00-1000796-20210610-170838"
      Xfile="convert_"+id+"-X.csv.gz" 
      yfile="convert_"+id+"-Y.txt"
      xtrain,ytrain=gettraining(Xfile,yfile,kick=kick)
      print(line)
      # print(xtrain.isnull().any(axis=1))
      xlist.append(xtrain)
      ylist.append(ytrain)
  l=len(xlist)
  klist=[]
  samplesize=[]
  Ytrain = pd.concat(ylist)
  Xtrain = pd.concat(xlist)
  #### Train transition and prior on Ytrain
  s_s=0
  w_w=0
  s_w=0
  w_s=0
  i=0
  # transition
  while i+1<len(Ytrain):
    if Ytrain[i]=="sleep":
      if Ytrain[i+1]=="sleep":
        s_s+=1
      else:
        s_w+=1
    else:
      if Ytrain[i+1]=="sleep":
        w_s+=1
      else:
        w_w+=1
    i+=1
  trans=np.array([[w_w/(w_s+w_w),w_s/(w_s+w_w)],[s_w/(s_s+s_w),s_s/(s_s+s_w)]])
  # Priors
  prior=np.array([1-sum(ytrain=="sleep")/len(ytrain),sum(ytrain=="sleep")/len(ytrain)])
  # Emissions cont
  rf_test=RandomForestClassifier(max_features='auto', n_estimators=ntree, n_jobs=4,
                         oob_score=True,verbose=3)
  rf_test.fit(Xtrain,Ytrain)
  if rf_test.classes_[1]!='sleep':
    raise ValueError('class labels issue')
  test=rf_test.predict_proba(Xtrain)[:,1]
  sleepdist=[i for i in test if i>0.5]
  s2s=np.mean(sleepdist)
  wakedist=[i for i in test if i<0.5]
  w2s=np.mean(wakedist)
  emis=np.array([[1-w2s,w2s],[1-s2s,s2s]])
  def betapara(x):
    n=len(x)
    x=[(x* (n-1)+0.5)/n for i in x]
    xbar=np.mean(x)
    vbar=np.var(x,ddof=1)
    alpha=xbar*(xbar*(1-xbar)/vbar-1)
    beta=(1-xbar)*(xbar*(1-xbar)/vbar-1)
    return alpha,beta
  asleep,bsleep=betapara(sleepdist)
  awake,bwake=betapara(wakedist)
  return trans,prior,asleep,bsleep,awake,bwake,emis
if __name__ == "__main__":
  para=trainpara("0610.txt")
  filehandler = open("hmmbeta.obj","wb")
  pickle.dump(para,filehandler)
# print("weighed average")
# print(akappa)