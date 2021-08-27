# Perform leave one out analysis
# Pseudocode
import sklearn.metrics
from rftest import *
import sys
import pandas as pd
from hmm import *
from hmm_cont import *
from window import *
import pickle
filelist=sys.argv[1]
ntree=sys.argv[2]
windowsize=sys.argv[3]
smoothing=sys.argv[4]
if len(sys.argv)==7:
  print('yi')
  kick=sys.argv[5]
  output=sys.argv[6]
else:
  kick=""
  output=sys.argv[5]

ntree=int(ntree)
windowsize=int(windowsize)
# filelist='test.txt'
def leaveoneout(filelist,smoothing='hmm',kick="",ntree=100,windowsize=10):
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
  balanceA=[]
  samplesize=[]
  for i in range(l):
    xmlist=xlist[:i]+xlist[i+1:]
    ymlist=ylist[:i]+ylist[i+1:]
    # print(xmlist)
    Xtraincombine = pd.concat(xmlist)
    Ytraincombine = pd.concat(ymlist)
    if len(set(Ytraincombine))==1 or len(set(ylist[i]))==1:
      print("singular value at "+str(i))
      continue
    rf_test=RandomForestClassifier(max_features='auto', n_estimators=ntree, n_jobs=4,
                         oob_score=True,verbose=3)
    rf_test.fit(Xtraincombine,Ytraincombine)
    ## Add HMM or other smoothing funciton here
    if smoothing=='hmm_cont':
      test=rf_test.predict_proba(xlist[i])[:,1]
      # with open("hmmcont.obj", "wb") as output_file:
        # pickle.dump([test], output_file)
      print(test)
      test=viterbi_cont(test)
      print(test)
      test=[['nosleep','sleep'][x] for x in test]
      test=np.array(test)
    else:
      test=rf_test.predict(xlist[i])
      print(test)
      if smoothing=="hmm":
        test=viterbi(test,["nosleep","sleep"], prior,trans,emis) #
      elif smoothing=='window':
        test=window_smoothing(test,windowsize)
      elif smoothing=='timevar':
        x=pd.DataFrame(ylist[i])
        x['groundtruth']=test
        test=x['groundtruth']
        test=viterbi_time(test)
        test=np.array(test)
      elif smoothing=='none':
        test=test
    print(ylist[i].values.shape)
    print(test.shape)
    klist.append(sklearn.metrics.cohen_kappa_score(ylist[i].values,test))
    balanceA.append(sklearn.metrics.balanced_accuracy_score(ylist[i].values,test))
    samplesize.append(test.shape[0])
  return klist,samplesize,balanceA
if __name__ == "__main__":
  klist,samplesize,balanceA=leaveoneout(filelist,smoothing,kick,ntree,windowsize)
  print(klist)
  if klist==[]:
    raise ValueError("no valid results")
  # wakappa=np.average(klist,weights=samplesize)
  akappa=np.average(klist)
  abalance=np.average(balanceA)
  with open(output,'a') as f:
    f.write(filelist+'\t'+str(smoothing)+'\t'+str(ntree)+'\t'+kick+'\t'+str(akappa)+'\t'+str(abalance)+'\t'+str(windowsize)+'\n')
# print("weighed average")
# print(akappa)