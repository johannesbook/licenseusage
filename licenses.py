#checking license usage @ Lundinova during 2023
#Johannes Book 2024..

from dash import dcc
import plotly.express as px
import pandas
from datetime import datetime
from datetime import timedelta
date_format = '%d/%m/%Y %I:%M:%S %p'
startDate = datetime(2023, 1, 1, 0, 0)

#Import data to matrix
df = pandas.read_csv('./UsageLog2023.csv',header=None)
data = []
for i in df.index:
    data.append(df[0][i].split(";"))

#initialize out matrices, to be used for plotting data. One value per hour. 
full = [] #Full licenses
#se = [] #Sch only licenses
for h in range(365*24):
    full.append(0)
#    se.append(0)

#clean up data, calculate max #licenses used every hour for plotting 
#start with hour blocks to save memory, try finer resolution later

for row in data:
    license = row[1]
    user = row[2]
    hogTime = datetime.strptime(row[5],date_format)
    releaseTime = datetime.strptime(row[6],date_format)
    hogHour = round((hogTime - startDate).total_seconds()/3600) #with hour 0 being 2023-01-01 00:00:00 etc
    releaseHour = round((releaseTime - startDate).total_seconds()/3600)
    for h in range(hogHour,releaseHour):
        full[h] = full[h] + 1 #one more license used during this period

#out[hogTime.hour][]
#print(hogTime)
#print(hogHour)
#print(releaseHour)
#print(releaseTime)

#Plot hoglevel

fig = px.histogram(full)
fig.show()

#count = 0
#h = 0
#for hogLevel in full:
    #h = h + 1
    #if hogLevel == 10:
        #print()
        #count = count +1
        #print(startDate + timedelta(hours=h))
