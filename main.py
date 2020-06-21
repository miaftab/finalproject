import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import matplotlib.patches as mpatches
import datetime
import requests
import csv
import os

# Function responsible for plotting the data over days
def plotChartFunction(x_dates,setData,title):

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




# Total No of cases in each provence over time
# iterate through each provence
for prov in provences:

    # Exclude Canada
    if prov != 'Canada':
        # add province name as key and empty list as value
        eachProviceCases[prov] = []

        # append list of zeros equal to no of dates against province
        for d in date:
            eachProviceCases[prov].append(0)

        for index,d in enumerate(date): # iterate on sorted date list
            for idx,da in enumerate(data["date"]): # match it within date column of data
                if da == d and prov == data['prname'][idx]: # if date match and province name is equal
                    eachProviceCases[prov][index] = int(data['numtotal'][idx]) # add data against province for given date
                    break

# plot graph Total No of cases in each provence over time
plotChartFunction(x_dates,eachProviceCases,'Total No of cases in each provence over time')




#Total No of cases tested each provence over time
eachProviceTestedCases = {}

# iterate through each provence
for prov in provences:

    # Exclude Canada
    if prov != 'Canada':

        # add province name as key and empty list as value
        eachProviceTestedCases[prov] = []

        # append list of zeros equal to no of dates against province
        for d in date:
            eachProviceTestedCases[prov].append(0)

        for index,d in enumerate(date):  # iterate on sorted date list
            for idx,da in enumerate(data["date"]):  # match it within date column of data
                if da == d and prov == data['prname'][idx]: # if date match and province name is equal
                    if data['numtested'][idx] != '':
                        eachProviceTestedCases[prov][index] = int(data['numtested'][idx])  # add data against province for given date
                    else:
                        eachProviceTestedCases[prov][index] = 0
                    break
# plot graph Total No of cases tested each provence over time
plotChartFunction(x_dates,eachProviceTestedCases,'Total No of cases tested each provence over time')




# No of new cases per day each provence over time
newCasesPerDay = {}

# iterate through each provence
for prov in provences:

    # Exclude Canada
    if prov != 'Canada':

        # add province name as key and empty list as value
        newCasesPerDay[prov] = []

        # append list of zeros equal to no of dates against province
        for d in date:
            newCasesPerDay[prov].append(0)

        for index,d in enumerate(date): # iterate on sorted date list
            for idx,da in enumerate(data["date"]):  # match it within date column of data
                if da == d and prov == data['prname'][idx]: # if date match and province name is equal
                    if data['numtested'][idx] != '':
                        newCasesPerDay[prov][index] = int(data['numtoday'][idx]) # add data against province for given date
                    else:
                        newCasesPerDay[prov][index] = 0
                    break

plotChartFunction(x_dates,newCasesPerDay,'No of new cases per day each provence over time')
# plot graph Total No of new cases per day each provence over time

try:
    os.remove("output.txt")
except:
    print("File not exist")

os.system("bash doubling.sh  Canada 'number of cases' 01-04-2020")
os.system("bash doubling.sh  Alberta 'number of cases' 01-04-2020")
os.system("bash doubling.sh  Ontario 'number of cases' 01-04-2020")

f = open("output.txt", "r")
prvinceName = []
NoOfDays=[]
legends=[]
colors = ['r','g','b']
index=0
for x in f:
    temp = x.split(" ")
    a=mpatches.Patch(color=colors[index],linestyle='--',label=temp[0]+'('+temp[2]+') --> '+'('+temp[4]+')')
    legends.append(a)
    prvinceName.append(temp[0]+'('+temp[1]+')')
    NoOfDays.append(int(temp[5].replace('\n', '')))
    index=index+1
print(prvinceName)
print(NoOfDays)

barlist=plt.bar(prvinceName,NoOfDays)
barlist[0].set_color('r')
barlist[1].set_color('g')
barlist[2].set_color('b')

plt.legend(handles=legends)
plt.title('Doubling Rate From Given Date')
plt.xlabel('Provinces From Date')
plt.ylabel('No Of Days')

plt.show()