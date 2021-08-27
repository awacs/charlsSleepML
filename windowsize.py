import sys
import pandas as pd
# filelist=sys.argv[1]
# mode=sys.argv[2] # average or weighed
file='RFwindowsize.out'
mode='average2'
name='accuracy'
a=pd.read_csv(file,header=None,sep='\t')
a.index=a.iloc[:,6]
a=a.sort_index()
if mode=="average":
  i=5
else:
  i=4
a[name]=a.iloc[:,i]
data=a[[name]]
print(data.index)
print(data)
import matplotlib.pyplot as plt
ax=data.plot.line(legend=False)
ax.set_xlabel("window size in minutes")
ax.set_ylabel("kappa")
plt.savefig('windowsize.png', bbox_inches="tight")
