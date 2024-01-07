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
hoursAtNine = 0
duplicateCounts = {}
duplicateHours = 0
hourOfDay = [0]*24
weekDay = [0]*7
userHours = {}

for row in data:
    counts = {}
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
            hour = int(out[h]["time"].strftime("%H"))
            hourOfDay[hour] += 1
            weekDay[int(out[h]["time"].weekday())] += 1

            #user toplist
            if hour > 7 and hour < 17: #(disregard off-hours work since it usually is pc's left on)
                if user not in userHours:
                    userHours[user] = 1
                else:
                    userHours[user] = userHours.get(user) + 1

            #how many hours are att full allocation, and any double-licence-hoggers? 
            if out[h]["count"] == 9:  
                hoursAtNine = hoursAtNine + 1
                #print("Full allocation!")
                #figure out if this is with duplicate user
                users = out[h]["who"].split("<br>")
                users.pop(0)
                for user in users:
                    if user not in duplicateCounts:
                        duplicateCounts[user] = 0
                    duplicateCounts[user] += 1
                    if duplicateCounts[user] > 1:
                        #print("...but ",user," has ",duplicateCounts[user]," licenses hogged.")
                        duplicateHours += 1
                duplicateCounts.clear()

#Plot and print
print("During 2023,",hoursAtNine,"hours spent @ 9 licenses used. Hoever, during these hours",duplicateHours,"were with someone hogging more than one license")
fig = px.bar(out.values(),x="time",y="count",hover_data="who",title="Allocation 2023")
fig.show()
fig = px.bar(hourOfDay,title="Usage during the day")
fig.show()
fig = px.bar(weekDay,title="Usage during the week")
fig.show()
fig = px.bar(x=userHours.keys(), y=userHours.values(), title="Hours with a license, total")
fig.show()


#backlog
#test second-level resolution
