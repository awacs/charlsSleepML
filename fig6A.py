import sys
import pandas as pd
# filelist=sys.argv[1]
# mode=sys.argv[2] # average or weighed
filelist='out.txt'
mode='average'
data=""
with open(filelist,'r') as f:
  for line in f:
    file=line.rstrip()
    name=file.split(".")[0]
    suffix=""
    if "rf" in file:
      suffix="rf"
    a=pd.read_csv(file,header=None,sep='\t')
    a.index=a.iloc[:,2]
    # a.index.name=None
    print(a)
    if mode=="average":
      i=4
    else:
      i=5
    a[name]=a.iloc[:,i]
    if isinstance(data,str):
      data=a[[name]]      
    else:
      data=data.join(a[[name]])
data=data.sort_index()
print(data.index)
print(data)
import matplotlib.pyplot as plt
ax=data.plot.line()
ax.set_xlabel("Number of trees in random forest")
ax.set_ylabel("kappa")
ax.legend(['Raw random forest',"HMM_beta",'HMM',"Window","HMM time variant"])
plt.savefig('6A_kai.png', bbox_inches="tight")
## Note, x axis need fix