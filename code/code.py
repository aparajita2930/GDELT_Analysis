import pandas as pd
import numpy as np
import glob
import os
from geopy.distance import great_circle

path = r'/home/aparajita/di/data'
files = glob.glob(os.path.join(path, "*.csv"))
df_each = (pd.read_csv(f) for f in files)
df = pd.concat(df_each, ignore_index = True)

print 'Median trip duration in seconds: '
print "{0:.10f}".format(df['tripduration'].median(axis=0))
#Output: 636.0000000000


print 'Fraction of rides that start and end at the same station: '
print "{0:.10f}".format(df[df['start station id']==df['end station id']].shape[0]/float(df.shape[0]))
#Output: 0.0212718740


print 'Standard deviation of the number of stations visited by a bike: '
df1 = df[['bikeid','start station id']]
df2 = df[['bikeid','end station id']]
df1.rename(columns={"bikeid":"bikeid","start station id":"stationid"},inplace=True)
df2.rename(columns={"bikeid":"bikeid","end station id":"stationid"},inplace=True)
df3=df1.append(df2)
df4=df3.groupby(['bikeid'])['stationid'].apply(lambda x: len(x.unique()))
print "{0:.10f}".format(df4.std(ddof=0))
#Output: 92.9870236190


print 'Average length, in kilometers, of a trip: '
df_neq = df[(df['start station id'] != df['end station id']) & (df['start station latitude'] >= -90)  & (df['start station latitude'] <= 90) & (df['start station longitude'] >= -180)  & (df['start station longitude'] <= 180) & (df['end station latitude'] >= -90)  & (df['end station latitude'] <= 90) & (df['end station longitude'] >= -180)  & (df['end station longitude'] <= 180)]
df_neq['stationdistance']=df_neq.apply(lambda x: great_circle((x['start station latitude'],x['start station longitude']),(x['end station latitude'],x['end station longitude'])).kilometers, axis=1)
print "{0:.10f}".format(df_neq['stationdistance'].mean(axis=0))
#Output: 1.8431122533


print 'Difference between the longest and shortest average durations in seconds: '
df['starttime'] = pd.to_datetime(df['starttime'],errors='coerce')
df['ym'] = df.starttime.dt.to_period("M")
mean_val = df.groupby(['ym'])['tripduration'].mean()
print "{0:.10f}".format(mean_val.max() - mean_val.min())
#Output: 430.5702959700


print 'Largest ratio of station hourly usage fraction to system hourly usage fraction: '
station = df.groupby(['start station id',df['starttime'].dt.hour]).size()/df.groupby(['start station id']).size()
system = df.groupby(df['starttime'].dt.hour).size()/float(df.shape[0])
print "{0:.10f}".format((station/system).max())
#output: 31.8123224883


print 'Fraction of rides that exceed their corresponding time limit: '
print "{0:.10f}".format(df[((df['usertype']=='Customer') & (df['tripduration']>30.0*60.0)) | ((df['usertype']=='Subscriber') & (df['tripduration']>45.0*60.0))].shape[0]/float(df.shape[0]))
#Output: 0.0371562890


print 'Average number of times a bike is moved during this period: '
df_new = df[['bikeid','starttime','start station id','end station id']]
df_new.sort_values(['bikeid','starttime'],ascending=[True,True],inplace=True)
print "{0:.10f}".format((df_new[df_new['start station id']!=df_new['end station id'].shift()].groupby(['bikeid'])['start station id'].count()-1).sum()/float(len(df_new['bikeid'].unique())))
#Output: 239.2490179958

