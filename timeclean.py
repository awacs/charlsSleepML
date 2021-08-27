import pytz
utc=pytz.utc
import datetime
import sys
def strfill(str):
  str=str.replace(" ", "")
  num=int(str)
  out="{:02d}".format(num)
  if len(out)!=2:
    raise ValueError('more than 2 characters')
  return out
import sys
input=sys.argv[1]
def timecheck(str):
  if ":" in str:
    h,m=str.split(':')
    h=strfill(h)
    m=strfill(m)
  elif '.' in str:
    h,m=str.split('.')
    h=strfill(h)
    m=strfill(m)
  elif str.isdecimal():
    if len(str)==4:
      h=str[0:2]
      m=str[2:4]
    elif len(str)==3:
      h=str[0:1]
      h=strfill(h)
      m=str[1:3]
    else:
      print(str)
      raise ValueError("string length weird")
  else:
    print(str)
    raise ValueError('string cannot be converted into time')
  return h+':'+m

def datecheck(str,year='2021'):
  if '.' in str:
    h,m=str.split('.')
    h=strfill(h)
    m=strfill(m)
  elif '/' in str:
    h,m=str.split('/')
    h=strfill(h)
    m=strfill(m)
  elif str.isdecimal():
    if len(str)==4:
      h=str[0:2]
      m=str[2:4]
    elif len(str)==3:
      h=str[0:1]
      h=strfill(h)
      m=str[1:3]
    elif len(str)==2:
      h=str[0]
      m=str[1]
      h=strfill(h)
      m=strfill(m)
    else:
      print(str)
      raise ValueError("string length weird")
  else:
    print('.' in str)
    print(line)
    raise ValueError('string cannot be converted into date')
  if int(h)<0 or int(h)>12:
    print(h)
    raise ValueError("this is not a right month")
  if int(m)<0 or int(m)>31:
    print(m)
    raise ValueError('this is not the right date')
  return year+'/'+h+'/'+m
  
with open(input,'r') as f:
  f.readline()
  for line in f:
    dat=line.rstrip().split('\t')
    dat[0]=datecheck(dat[0])
    dat[2]=timecheck(dat[2])
    dat[3]=datecheck(dat[3])
    dat[5]=timecheck(dat[5])
    print("\t".join(dat))
    try:
      s=utc.localize(datetime.datetime.strptime(dat[0]+' '+dat[2], '%Y/%m/%d %H:%M'))
    except:
      print(dat[0]+' '+dat[2])
    e=utc.localize(datetime.datetime.strptime(dat[3]+' '+dat[5], '%Y/%m/%d %H:%M'))
    print (e-s)
    if s>e:
      print(s)
      print(e)
      print(line)
      raise ValueError
