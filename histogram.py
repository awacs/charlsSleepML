# Perform leave one out analysis
# Pseudocode
import sklearn.metrics
from rftest import *
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from hmm import *
from hmm_cont import *
from window import *
import pickle
from itertools import groupby


# filelist='test.txt'
def runlength(x,labels,output):
  print('x')
  lst=[]
  print('y')
  for i in x:
    print(lst)
    b=[(k, sum(1 for i in g)) for k,g in groupby(i)]
    print('a')
    c=pd.DataFrame(b)
    print('b')
    d=c.loc[c.iloc[:,0]=='sleep'].iloc[:,1]
    print('c')
    lst.append(d.values/120)
  plt.clf()
  plt.ylim(0,400)
  bins = np.linspace(0, 12, 13)
  plt.hist(lst, bins,label=labels)
  plt.legend(loc='upper right')
  plt.xticks(bins)
  plt.xlabel('hours')
  plt.savefig(output, bbox_inches="tight")

def applymodel(filelist,model,kick=''):
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
  Xtraincombine = pd.concat(xlist)
  Ytraincombine = pd.concat(ylist)
  with open(model, "rb") as input_file:
    para = pickle.load(input_file)
  rf,ntree,windowsize=para
  test_hmmcont=rf.predict_proba(Xtraincombine)[:,1]
  test_hmmcont=viterbi_cont(test_hmmcont)
  test_hmmcont=[['nosleep','sleep'][x] for x in test_hmmcont]
  test_hmmcont=np.array(test_hmmcont)
  test=rf.predict(Xtraincombine)
  test_hmm=viterbi(test,["nosleep","sleep"], prior,trans,emis) #
  test=rf.predict(Xtraincombine)
  test_window=window_smoothing(test,windowsize)
  test=rf.predict(Xtraincombine)
  x=pd.DataFrame(Ytraincombine)
  x['groundtruth']=test
  test=x['groundtruth']
  test_timevar=viterbi_time(test)
  test=rf.predict(Xtraincombine)
  return test,test_hmm,test_timevar,test_window,test_hmmcont,Ytraincombine.values
if __name__ == "__main__":
  filelist=sys.argv[1]
  model=sys.argv[2]
  if len(sys.argv)==5:
    print('yi')
    kick=sys.argv[3]
    output=sys.argv[4]
  else:
    kick=""
    output=sys.argv[3]
  a=applymodel(filelist,model,kick)
  runlength(a,['Raw random forest','HMM','HMM time variant','Window','HMM_beta','Groundtruth'],output)
# print("weighed average")
# print(akappa)