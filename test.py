import math
import os

import show
import process

dest_dir = "./backup/Juni/"
files = os.listdir(dest_dir)
newFiles = []
for file in files:
    if ".log" in file:
        newFiles.append(dest_dir+file)

newFiles=[]
newFiles.append("ping.log")

minutes = 5

for file in newFiles:
    name = file.replace(".log", ".png")
    print(file)
    data = process.get_averaged_date(file, minutes, show_milliseconds=True)
    divisor = math.log(minutes)
    if divisor == 0:
        divisor = 1/2
    show.plot(data=data, file=name)
