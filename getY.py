import pandas as pd
import sys
import pytz
utc=pytz.utc
import datetime
epoch=sys.argv[1]
record=sys.argv[2]
# id=sys.argv[3]
output=sys.argv[3]
fak = lambda x: ' '.join(x.split(' ')[0:2])
class Timeinterval:
  def __init__(self,start,end):
    self.start=start
    self.end=end
    if start>end:
      print("error")
      print(start)
      print(end)
      raise ValueError
  def __eq__(self,query):
    if self.start<=query and query<=self.end:
      return True
    else:
      return False
  def __repr__(self):
    repr=self.start.strftime("%m/%d/%Y %H:%M:%S")+'--'+self.end.strftime("%m/%d/%Y %H:%M:%S")
    return(repr)
def getTruth(epoch,record):
  # epoch="convert_MATA00-1000079-20210524-143705-epoch.csv.gz"
  id=epoch.split('-')[1]
  # print(id)
  ep=pd.read_csv(epoch, header=0)
  sleep_intervals=[]
  start=''
  end=''
  
  with open(record,'r') as f:
    for line in f:
      # print(id)
      [sdate,_,stime,edate,_,etime,ID]=line.rstrip().split('\t')
      # print(ID)
      if ID==id:
        print(line)
        s=utc.localize(datetime.datetime.strptime(sdate+' '+stime, '%Y/%m/%d %H:%M'))
        e=utc.localize(datetime.datetime.strptime(edate+' '+etime, '%Y/%m/%d %H:%M'))
        sleep_intervals.append(Timeinterval(s,e))
        # print(s)
        if start=="":
          start=s
          end=e
        else:
          if s<start:
            start=s
          if e>end:
            end=e
  if start=="":
    raise ValueError("potential sleep record wrong file")
  sleep_groundtruth= pd.DataFrame(index=ep.index, columns=['time','groundtruth','id'])
  sleep_groundtruth['time']=ep['time']
  # print('hey')
  # print(start)
  # print(end)
  for i in range(ep.shape[0]):
    t=ep.loc[i,'time']
    # print(t)
    x=pd.to_datetime(fak(t))
    print(x)
    print(start)
    sleep_groundtruth.loc[i,'id']=id
    if x > start and x<end:
      if x in sleep_intervals:
        sleep_groundtruth.loc[i,'groundtruth']='sleep' # change for plotting
      else:
        sleep_groundtruth.loc[i,'groundtruth']='nosleep'
    else:
      sleep_groundtruth.loc[i,'groundtruth']='outside'
  return sleep_groundtruth
groundtruth=getTruth(epoch,record)
groundtruth.to_csv(output, index=0)