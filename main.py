import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import matplotlib.patches as mpatches
import datetime
import requests
import csv
import os

# plot chart on SetData
x_dates = date2num(x_dates)
ax = plt.subplot(111)
legends = []

# Colors Array
colors = ['orange',
        'green',
        'red',
        'blue',
        'purple',
        'yellow',
        'grey',
        'magenta',
        'black',
        'cyan',
        'brown',
        'indigo',
        'olive',
        'navy',
        'orchid'
        ]

count = 0

# DataSet have key as each provence name and it's data list as value
for key,value in setData.items():
ax.plot(x_dates, value, color=colors[count])
a=mpatches.Patch(color=colors[count],linestyle='--',label=key)
legends.append(a)
count = count + 1
ax.xaxis_date()
plt.legend(handles=legends)
plt.title(title,size=10,color='Green')
plt.show()



# Remove old CSV with name covid19 if exits
try:
os.remove("covid19.csv")
except:
print("File not exist")



# Download new covid19 csv from HIC website
req = requests.get("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv")
url_content = req.content
csv_file = open('covid19.csv', 'wb')
csv_file.write(url_content)
csv_file.close()


# open the file
with open('covid19.csv', 'r') as infile:
# read the file as a dictionary for each row ({header : value})
reader = csv.DictReader(infile)
data = {}
for row in reader:
for header, value in row.items():
    try:
        data[header].append(value)
    except KeyError:
        data[header] = [value]



# extract the variables you want
provences = list(set(data['prname']))
totalCases = data['numtotal']

# Select only unique dates sorted
date = list(set(data['date']))
date = sorted(date, key=lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))



# Extracting dates and converting it to date time object
x_dates = []
eachProviceCases = {}

# append Unique dates in x_dates
for d in date:
splitedDate = d.split('-')
temp = datetime.date(int(splitedDate[2]),int(splitedDate[1]),int(splitedDate[0]))
x_dates.append(temp)