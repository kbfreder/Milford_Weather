import matplotlib.pyplot as plt
#import mplleaflet#not loaded in Canopy
import pandas as pd
import numpy as np
import datetime as dt

df = pd.read_csv('weather data_cleaned.csv')

#convert Temp to C (it is in tenth of degree Celciuis) & rename column
df['Value'] /= 10
df.rename(columns={'Value': 'Temp'}, inplace = True)

#Pull out Month & Day & Year
df['Year'] = df['Date'].map(lambda x: dt.datetime.strptime(x,"%Y-%m-%d").year)
df['Month'] = df['Date'].map(lambda x: dt.datetime.strptime(x,"%Y-%m-%d").month)
df['Day'] = df['Date'].map(lambda x: dt.datetime.strptime(x,"%Y-%m-%d").day)

#drop Feb 29:
df.drop(df[(df['Month'] == 2) & (df['Day'] == 29)].index, inplace=True)


#Get Tmax & Tmin for each day, for 2005-2014
tmax_grouped = df[(df['Year'] < 2015) & (df['Element'] == 'TMAX')].groupby(['Month', 'Day'])['Temp'].max()
tmax = tmax_grouped.ravel()
tmin_grouped = df[(df['Year'] < 2015) & (df['Element'] == 'TMIN')].groupby(['Month', 'Day'])['Temp'].min()
tmin = tmin_grouped.ravel()


#2015 data
tmax_2015_grouped = df[(df['Year'] == 2015) & (df['Element'] == 'TMAX')].groupby(['Month', 'Day'])['Temp'].max()
tmax_2015 = tmax_2015_grouped.ravel()

tmin_2015_grouped = df[(df['Year'] == 2015) & (df['Element'] == 'TMIN')].groupby(['Month', 'Day'])['Temp'].min()
tmin_2015 = tmin_2015_grouped.ravel()


#pull 2015 data that is greater/less than 2005-2014 max/mins:
tmax_2015_to_plot = []
tmin_2015_to_plot = []

for i in range(365):
    if tmax_2015[i] > tmax[i]:
        tmax_2015_to_plot.append([i, tmax_2015[i]])
    if tmin_2015[i] < tmin[i]:
        tmin_2015_to_plot.append([i, tmin_2015[i]])



#PLOT THIS SHIT
maxx, maxy = zip(*tmax_2015_to_plot)
minx, miny = zip(*tmin_2015_to_plot)

fig = plt.figure()
plt.plot(tmax, label='Historical Max',color = 'salmon')
plt.plot(tmin, label='Historical Min', color = '#6699ff')
plt.gca().fill_between(range(len(tmax)), 
                       tmin, tmax, 
                       facecolor='tan', 
                       alpha=0.25)

plt.scatter(maxx, maxy, s=50, color = 'red', label = '2015 Max new record')
plt.scatter(minx, miny, s=50, color = 'blue', label = '2015 Min new record')
plt.legend(loc=8, scatterpoints=1, fontsize ='small')
plt.title("Temperature Data for Milford, CT")
plt.ylabel("Temp (C)")
labels = ['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec']
plt.xticks(np.arange(15,365, 365/12), labels)
plt.xlabel('')

