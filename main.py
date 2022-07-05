import os
import time

import subprocess
from dateutil import parser
from datetime import datetime


def format_entry(time_stamp: datetime, message: str):
    return str.format('{time};{message}', time=time_stamp.strftime("%d.%m.%Y %H:%M:%S"), message=message)


def ping():
    ping_starttime = datetime.now()
    try:
        result = subprocess.run(['ping', '-c', '1', "1.1.1.1"], text=True, capture_output=True, check=True)
    except Exception:
        return -1

    for line in result.stdout.splitlines():
        if "icmp_seq" in line:
            timing = line.split('=')[-1].split(' ms')[0]
            return ping_starttime, timing


class PingLogger:
    data = {}

    def gen_ping(self):
        while True:
            result = ping()
            #print('Returning', result)
            yield result
            time.sleep(10)

    def log(self, time_stamp: datetime, message: str):
        with open('ping.log', mode='a+') as file:
            file.write(format_entry(time_stamp, message)+'\n')
        self.data[time_stamp] = message

        if len(self.data.keys()) > 15000:
            self.backup()

    def backup(self):
        while len(self.data.keys()) > 15000:
            if not os.path.isdir("backup"):
                os.mkdir("backup")
            date = parser.parse(list(self.data.keys())[10000].split(";")[0], dayfirst=True)
            #print("Backing up")
            old_timestamps = self.data.keys()[:10000]
            with open("./backup/ping_backup_" + date.strftime("%d.%m.%Y_%H-%M-%S") + ".log", 'w') as newFile:
                for timestamp in old_timestamps:
                    newFile.write(format_entry(timestamp, self.data[timestamp]) + "\n")
                    self.data.pop(timestamp)

        with open("ping.log", 'w') as file:
            for timestamp in self.data.keys():
                file.write(format_entry(timestamp, self.data[timestamp]) + "\n")

    def log_gen(self, gen):
        for result in gen:
            try:
                time_stamp, timing = result
            except Exception:
                continue

            #print("Zeit", timing, "ms")

            message = timing
            if timing == -1:
                message = 2000

            self.log(time_stamp, message)

            yield self.data

    def run(self, gen):
        if gen is None:
            gen = self.gen_ping()
        self.data = {}

        log = self.log_gen(gen)
        for i in log:
            continue


if __name__ == '__main__':
    logger = PingLogger()
    logger.run(None)
