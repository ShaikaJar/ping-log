import time

import subprocess
import logging
from dateutil import parser


def ping():
    try:
        result = subprocess.run(['ping', '-c', '1', "1.1.1.1"], text=True, capture_output=True, check=True)
    except:
        return -1

    for line in result.stdout.splitlines():
        if "icmp_seq" in line:
            timing = line.split('time=')[-1].split('Zeit=')[-1].split(' ms')[0]
            return timing


logging.basicConfig(filename="ping.log", level=logging.DEBUG, format='%(asctime)s;%(message)s', datefmt="%d.%m.%Y %H:%M:%S", filemode='a+')



while True:
    t = ping()
    if t == -1:
        logging.error(2000)
    else:
        logging.debug(t)
    print("Zeit", t, "ms")

    lines = []
    with open("ping.log") as file:
        content = file.read()
        lines = content.split("\n")
    if len(lines) > 15000:
        while len(lines) > 15000:
            date = parser.parse(lines[10000].split(";")[0], dayfirst=True)
            print("Backing up")
            oldLines = lines[:10000]
            newLines = lines[10000:]
            with open("./backup/ping_backup_"+date.strftime("%d.%m.%Y_%H-%M-%S")+".log", 'w') as newFile:
                for line in oldLines:
                    newFile.write(line+"\n")
            lines = newLines

        with open("ping.log", 'w') as file:
            for line in lines:
                file.write(line+"\n")

    time.sleep(10)