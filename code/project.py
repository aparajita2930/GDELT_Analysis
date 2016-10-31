import pandas as pd
%pylab

df = pd.read_csv('gdelt.TXT',nrows=10000000,delimiter='\t')

#Top 20 most recurring events:
rec_events = df.groupby(['CAMEOCode']).size()
rec_events.sort_values(ascending=False,inplace=True)
rec_events = rec_events[0:20]
rec_events=rec_events.rename('RecurringEvents')
figure(1),rec_events.plot.pie(figsize=(6,6),autopct='%.2f')

#Top 20 most significant events:
sig_events = df.groupby(['CAMEOCode'])['NumArts'].sum()
sig_events.sort_values(ascending=False,inplace=True)
sig_events=sig_events[0:20]
sig_events=sig_events.rename('SignificantEvents')
figure(2),sig_events.plot.pie(figsize=(6,6),autopct='%.2f')

#Check if being a recurrent event is correlated to being an event of significance
corr_val = rec_events.corr(sig_events) #Compute Pearson's correlation coefficient
print "{0:.10f}".format(corr_val)

#Countries having material conflicts
df.groupby(['QuadClass'])['Source','Target','SourceGeoLat','SourceGeoLong','TargetGeoLat','TargetGeoLong'].get_group(4).dropna().to_csv('quadloc.csv',index=False)

#Countries with whom USA has any sort of action
df_usa=df[(df['Source']=='USA')|(df['Target']=='USA')]
df_usa[['SourceGeoLat','SourceGeoLong','TargetGeoLat','TargetGeoLong']].dropna().to_csv('locdata.csv',index=False)
