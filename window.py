import statistics
from statistics import mode
import numpy as np
def window_smoothing(signal,u=1):
  l=len(signal)
  smoothed=signal.copy()
  i=0
  while i<l:
    left=max(0,i-u)
    right=min(i+u+1,l)
    window=signal[left:right]
    sig=mode(window)
    smoothed[i]=sig
    i+=1
  return(smoothed)

if __name__ == "__main__":
   V=np.array(list('xyxyyxyxyyyyxxxxxxxyyyyyyyy'))
   print(window_smoothing(V,2))