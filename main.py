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
    plt.xticks(rotation=70)
    plt.legend(handles=legends)
    plt.title(title,size=10,color='Green')
    plt.show()


# Question No 1
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

# open the file and read
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



# extract the variables you want unique
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


# Question No 2
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
print(x_dates)
print(eachProviceCases)


# Question No 3
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



# Question No 4
# No of new cases per day each provence over time
newCasesPerDay = {}
dates = set()
# iterate through each provence
for prov in provences:

    # Exclude Canada
    if prov != 'Canada':

        # add province name as key and empty list as value
        newCasesPerDay[prov] = []

        for index,d in enumerate(date): # iterate on sorted date list

            proceed = False
            # check if all provinces have zero data for a specific date
            for idx2,checkDate in enumerate(data["date"]):
                if checkDate == d and int(data['numtoday'][idx2]) > 50:
                    proceed = True
                    break

            if proceed:
                dates.add(d)
                ignore = False
                for idx,da in enumerate(data["date"]):  # match it within date column of data
                    if da == d and prov == data['prname'][idx]: # if date match and province name is equal
                        if data['numtoday'][idx] != '':
                            newCasesPerDay[prov].append(int(data['numtoday'][idx])) # add data against province for given date
                        else:
                            newCasesPerDay[prov].append(0)
                        ignore=True
                        break
                if not ignore:
                    newCasesPerDay[prov].append(0)

date = list(dates)
date = sorted(date, key=lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
x_dates = []
for d in date:
    splitedDate = d.split('-')
    temp = datetime.date(int(splitedDate[2]),int(splitedDate[1]),int(splitedDate[0]))
    x_dates.append(temp)


# plot graph Total No of new cases per day each provence over time
plotChartFunction(x_dates,newCasesPerDay,'No of new cases per day each provence over time')




# Question No 5
# calculates the doubling rate given arguments: province, variable
# containing number of cases or number of deaths, and a given
# date

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



#Free Choice

eachProviceCases={}
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

x_dates=[]

for i in range((0),14):
    d=datetime.datetime.now() + datetime.timedelta(days=i)
    x_dates.append(d.date())

for prov in provences:
    # Exclude Canada
    if prov != 'Canada':
        eachProviceCasesUpdated={}
        Stats = eachProviceCases[prov]
        last7Values=[]
        nextTwoWeekData=[]

        for i in range((0), len(Stats)):
            if i >= (len(Stats) - 7):
                last7Values.append(Stats[i])
        print(prov)
        print(last7Values)

        #generate next 2 week data
        for i in range((0),14):
            count=0
            sum=0
            for j in range((i+1),len(last7Values)):
               sum = sum + (last7Values[j] - last7Values[j-1])
               count=count+1
            last7Values.append(last7Values[len(last7Values)-1] + (sum/count))
            nextTwoWeekData.append(last7Values[len(last7Values)-1] + (sum/count))
            print(last7Values[len(last7Values)-1] + (sum/count))

        eachProviceCasesUpdated[prov] = nextTwoWeekData
        print(x_dates)
        print(eachProviceCasesUpdated)
        plotChartFunction(x_dates,eachProviceCasesUpdated,'No of cases in '+prov+' forecast data')


