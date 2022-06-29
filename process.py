import datetime
import math

from dateutil import parser



def get_data_old():
    with open('ping.log') as file:
        content = file.read()
        lines = content.split("\n")
        data = {}
        for line in lines:
            if not line:
                continue
            entry = line.split(" | ")
            # print(entry)
            entry[0] = entry[0].replace(',', '.')
            entry[1] = entry[1].replace('ms', '').strip()
            pingT: int = 0
            if entry[1] == "No Connection":
                pingT = 2000
            else:
                pingT = math.floor(float(entry[1]))

            trueDateTime = parser.parse(entry[0])
            dateTime = trueDateTime.strftime("%d.%m.%Y %H:%M:%S")
            # dateTime = trueDateTime.hour+":"+trueDateTime.minute+" Uhr "+trueDateTime.day+"."+trueDateTime.month+"."
            data[dateTime] = pingT
        return data


def get_data(filename: str, fill_in_minutes: int = 1, ping:bool=False, max_minutes_ago:int=0):
    parser.parserinfo(dayfirst=True)
    with open(filename) as file:
        content = file.read()
        lines = content.split("\n")
        data = {}
        lastTime = 0
        for line in lines:
            if not line:
                continue
            entry = line.split(";")
            time = parser.parse(entry[0],dayfirst=True)

            if not (not lastTime):
                while (time - lastTime).total_seconds() > fill_in_minutes * 60:
                    lastTime = lastTime + datetime.timedelta(minutes=fill_in_minutes)
                    data[lastTime.strftime("%d.%m.%Y %H:%M:%S")] = -1

            pingT = math.floor(float(entry[1]))
            if not ping:
                if pingT == 2000:
                    pingT=1
                else:
                    pingT=0



            ago = (datetime.datetime.now()-time).total_seconds()/60
            print("Ago:",ago)
            if max_minutes_ago<=0 or ago<max_minutes_ago:
                data[time.strftime("%d.%m.%Y %H:%M:%S")] = pingT
                print("Added")
            else:
                print("Not Added")
            lastTime = time
        return data


def average(input: list):
    sum = 0
    for entry in input:
        sum += entry
    return sum / len(input)


def avg_data_minutes(dictionary: dict, minutes=1):
    newDict = {}
    for key in dictionary.keys():
        time = parser.parse(key,dayfirst=True)
        newKey = time.replace(minute=minutes * math.floor(time.minute / minutes)).strftime("%d.%m.%Y %H:%M")
        if newKey not in newDict.keys():
            newDict[newKey] = []
        newDict[newKey].append(dictionary[key])

    avgDict = {}
    for key in newDict.keys():
        avgDict[key] = average(newDict[key])
    return avgDict

def get_averaged_date(filename:str, minutes:int=1, ping=False):
    return avg_data_minutes(get_data(filename, minutes, ping=ping), minutes)


def write_to_dict(dictionary: dict, filename: str):
    with open(filename, 'w') as f:
        for key in dictionary.keys():
            f.write("%s;%s\n" % (key, dictionary[key]))


if __name__ == '__main__':
    write_to_dict(avg_data_minutes(get_data('ping.log', 5), 5), 'ping-log.csv')
