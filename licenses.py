#checking license usage @ Lundinova during 2023
#Johannes Book 2024..

import plotly.express as px
import pandas
from datetime import datetime
from datetime import timedelta
date_format = '%d/%m/%Y %I:%M:%S %p'
startDate = datetime(2023, 1, 1, 0, 0)
endDate = datetime(2024,1,1,0,0)

#Import data to matrix
df = pandas.read_csv('./UsageLog2023.csv',header=None)
data = []
for i in df.index:
    data.append(df[0][i].split(";"))

#initialize output dictionary, to be used for plotting
out = {}
for h in range(365*24): #number of hours during the year
    out[h] = {"count":0}
    out[h].update({"who":""})
    out[h]["time"] = startDate + timedelta(hours=h)

#clean up data, calculate max #licenses used every hour for plotting 
#start with hour blocks to save memory, perhaps try minute-resolution later to see if it makes any difference

for row in data:
    license = row[1]
    user = row[2]
    hogTime = datetime.strptime(row[5],date_format)
    releaseTime = datetime.strptime(row[6],date_format)
    hogHour = round((hogTime - startDate).total_seconds()/3600) #with hour 0 being 2023-01-01 00:00:00 etc
    releaseHour = round((releaseTime - startDate).total_seconds()/3600)
    if ((license != "RMVG-3AF3") and (license != "T439-P5NG") and (license != "PMAM-4M4E")): #do not include our viewer licenses in stats
        for h in range(hogHour,releaseHour):
            out[h]["count"] = out[h]["count"] + 1 
            out[h]["who"] = out[h]["who"] + "<br>" + user
            out[h]["time"] = startDate + timedelta(hours=h)

#Plot
hoverData = []
for val in out.values(): 
    hoverData.append(val["who"])
    
fig = px.line(out.values(),x="time",y="count",hover_data="who")
fig.show()

#backlog
#count number of hours of full usage
#display duplicate users (single user with more than one license)
#make graph look nicer
#display day of week
