import time

import matplotlib.pyplot as plt
from dateutil import parser
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
from http.server import HTTPServer, CGIHTTPRequestHandler
import _thread as thread

import process


def plot(data: dict, file:str = "test.png", figsize=(10,3)):
    labels = []
    values = []
    for key in data.keys():
        date = parser.parse(key, dayfirst=True)
        if date.month != 2:
            print(date.strftime("%d.%m.%Y %H:%M:%S"))
        labels.append(date)
        values.append(data[key])

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(labels, values, 1 / len(labels))
    ax.xaxis.set_major_locator(ticker.LinearLocator(30))
    ax.margins(x=0)
    ax.set_ylim(ymin=0)
    #ax.set_yscale("log")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %Hh"))

    ax.set(xlabel=str(len(labels)) + " Messpunkte", ylabel='ping (ms)', title='Ausfälle')
    # ax.set_xticks()
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    plt.tight_layout()

    fig.savefig(file)
    return plt


def plot_standard():
    while True:
        print("Fetching Data")
        data = process.get_data("ping.log", 5, max_minutes_ago=8*60)
        # print("Rounding Data")
        data = process.avg_data_minutes(data, 1)
        print("Plotting")
        plot(data=data)
        print("Plotted")
        time.sleep(60)


if __name__ == '__main__':
    thread.start_new_thread(plot_standard, ())
    print("Serving")
    os.chdir(".")
    server_object = HTTPServer(server_address=('', 8042), RequestHandlerClass=CGIHTTPRequestHandler)
    server_object.serve_forever()
