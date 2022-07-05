import datetime
import math

from dateutil import parser


def _average(input: list):
    sum = 0
    for entry in input:
        sum += entry
    return sum / len(input)


class DataProcessor:
    fill_in_minutes: int = 1
    show_milliseconds: bool = False
    max_minutes_ago: int = 0

    def __init__(self, fill_in_minutes: int = 1, show_milliseconds: bool = False, max_minutes_ago: int = 0):
        self.show_milliseconds = show_milliseconds
        self.fill_in_minutes = fill_in_minutes
        self.max_minutes_ago = max_minutes_ago

    raw_data = {}
    processed_data = {}

    def avg_process_generator(self, gen):
        for raw_data in gen:
            self.raw_data = raw_data
            self.process_raw_data()
            yield self.avg_processed_data()

    def read_file_raw(self, filename):
        parser.parserinfo(dayfirst=True)
        with open(filename) as file:
            content = file.read()
            lines = content.split("\n")
            return self.read_lines_raw(lines)

    def read_lines_raw(self, lines: list):
        for line in lines:
            if not line:
                continue
            entry = line.split(";")
            #print(entry[0])
            time = parser.parse(entry[0], dayfirst=True)
            pingT = math.floor(float(entry[1]))

            self.append_raw_data(time, pingT)
        return self.raw_data

    def append_raw_data(self, ping_timestamp: datetime.datetime, ping_timeout: int):
        self.raw_data[ping_timestamp] = ping_timeout

    def process_raw_data(self, raw_data=raw_data):
        self.raw_data = raw_data
        data = {}
        lastTime = None
        for time in self.raw_data.keys():
            ago = (datetime.datetime.now() - time).total_seconds() / 60
            if not (self.max_minutes_ago <= 0 or ago < self.max_minutes_ago):
                continue
            pingT = self.raw_data[time]

            if lastTime is not None:
                while (time - lastTime).total_seconds() > self.fill_in_minutes * 60:
                    lastTime = lastTime + datetime.timedelta(minutes=self.fill_in_minutes)
                    data[lastTime.strftime("%d.%m.%Y %H:%M:%S")] = -1

            if not self.show_milliseconds:
                if pingT == 2000:
                    pingT = 1
                else:
                    pingT = 0

            ago = (datetime.datetime.now() - time).total_seconds() / 60
            # #print("Ago:",ago)
            if self.max_minutes_ago <= 0 or ago < self.max_minutes_ago:
                data[time.strftime("%d.%m.%Y %H:%M:%S")] = pingT
                # #print("Added")
            # else:
            # #print("Not Added")
            lastTime = time

        self.processed_data = data
        return data


    def avg_processed_data(self, minutes=1):
        newDict = {}
        last_time_stemp:datetime.datetime=None
        last_value = 0
        for key in self.processed_data.keys():
            value = self.processed_data[key]
            time = parser.parse(key, dayfirst=True)
            if last_time_stemp is None:
                last_value = value
                last_time_stemp = time
                continue

            newKey = last_time_stemp.replace(minute=minutes * math.floor(time.minute / minutes)).strftime("%d.%m.%Y %H:%M")
            if newKey not in newDict.keys():
                newDict[newKey] = []
            #last_value *= math.fabs((last_time_stemp-time).total_seconds())/60
            newDict[newKey].append(last_value)

            last_value = value
            last_time_stemp = time

        avgDict = {}
        for key in newDict.keys():
            avgDict[key] = _average(newDict[key])

        return avgDict

    def old_avg_processed_data(self, minutes=1):
        newDict = {}
        last_value = 0
        last_time_stamp:datetime.datetime = None
        for key in self.processed_data.keys():
            time = parser.parse(key, dayfirst=True)
            value = self.processed_data[key]




            newKey = time.replace(minute=minutes * math.floor(time.minute / minutes)).strftime("%d.%m.%Y %H:%M")
            if newKey not in newDict.keys():
                newDict[newKey] = []
            newDict[newKey].append(value)

        avgDict = {}
        for key in newDict.keys():
            avgDict[key] = _average(newDict[key])

        return avgDict


def get_averaged_date(filename: str, minutes: int = 1, show_milliseconds=False):
    processor = DataProcessor(show_milliseconds=show_milliseconds)
    processor.read_file_raw(filename)
    processor.process_raw_data()
    return processor.avg_processed_data(minutes=minutes)
