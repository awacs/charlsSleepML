import argparse
import pandas as pd
import datetime
import pytz

parser = argparse.ArgumentParser(description="""Convert matrix raw data,
                            with 23 digits float timestamp.""")
parser.add_argument('inputFile', metavar='input file', type=str)
args = parser.parse_args()

split_pos = args.inputFile.rfind('/')

path = args.inputFile[:split_pos+1]
file_name = args.inputFile[split_pos+1:]
output_rows = None

# data = pd.read_csv(path+file_name, header=0, nrows=output_rows, usecols=list(range(4))+list(range(7,11)))
def unixToTimestamp(row):
    unix_ts = float(row['dateTime']/1000)
    tz = pytz.timezone('Asia/Shanghai')
    targetDate = datetime.datetime.fromtimestamp(unix_ts, tz=tz)
    tz = targetDate.tzinfo
    return "%s%s%s" % (
        targetDate.strftime('%Y-%m-%d %H:%M:%S'),
        str("%.3f" % (float( targetDate.microsecond / 1e6)))[1:5],
        targetDate.strftime(f'%z [{tz}]')
    )

def msAddTimezone(row, summerConvert=False):
    # input datetime with ms
    # if summerConvert=True, substract 1 hour
    if row['time'].count(".")==0:
      row['time']=row['time']+"."
    ms_dt_string = row['time'].ljust(23,'0')
    # print(ms_dt_string)
    if "T" in ms_dt_string:
      ms_dt_string=ms_dt_string.replace("T"," ")
    tz = '+0000 [UTC]'
    if summerConvert == True:
        ms_dt_ts = datetime.datetime.strptime(ms_dt_string, '%Y-%m-%d %H:%M:%S.%f')
        ms_dt_str_sc = (ms_dt_ts + datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S.%f")[0:23]
        return "%s%s" % (ms_dt_str_sc,tz)
    else:
        # s_dt_ts = datetime.datetime.strptime(ms_dt_string[:-3], '%Y-%m-%d %H:%M:%S.%f')
        return "%s%s" % (ms_dt_string,tz)

def matrix_axis_adjust(df):
    df_converted = df
    df_converted["acc_x"] = df_converted["acc_x"] * -1
    df_converted["acc_y"] = df_converted["acc_y"] * -1
    df[['acc_x', 'acc_y']] = df[['acc_y', 'acc_x']]

    return df_converted

def clip_interval(df, start, end):
    pass
chunksize = 10 ** 4
header=False
print(path+file_name)
with pd.read_csv(path+file_name, header=0, nrows=output_rows, chunksize=chunksize) as reader:  
  for data in reader:
    # process(data)
    # data = pd.read_csv(path+file_name, header=0, nrows=output_rows, usecols=list(range(7)))
    # data = pd.read_csv("test.csv", header=0, nrows=output_rows, usecols=list(range(7)))
    data["time"] = data.apply(msAddTimezone, axis=1, args=(False,))
    # data = matrix_axis_adjust(data)
    #print(data.describe())
    if header==False:
      data.to_csv(path+"convert_"+file_name, index=0)
      header=True
    else:
      data.to_csv(path+"convert_"+file_name, index=0, header=False, mode='a')
