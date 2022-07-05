import asyncio
import datetime
import math
import socketserver
import threading
import time

import matplotlib.pyplot as plt
from dateutil import parser
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
from http.server import HTTPServer, CGIHTTPRequestHandler, BaseHTTPRequestHandler
import _thread as thread
from process import DataProcessor

from main import PingLogger

import multiprocessing

import io


class Plotter:
    buff: bytes = None

    _raw_data = {}
    average_minutes = 1

    _max_render_timeout = 90

    def __init__(self, logger: PingLogger = PingLogger()):
        self._processor = DataProcessor(max_minutes_ago=1 * 60)

        self.logger = logger
        self._gen = self.logger.gen_ping()
        self.buff_gen = None

        self._process_thread = threading.Thread(target=self._data_from_gen, args=(self._gen,))
        self._process_thread.start()

        self._render_thread = threading.Thread(target=self.build_buf)
        self._render_thread.start()

    def send_trigger(self):
        try:
            self.buff_gen.send(0)
        except Exception:
            print('Already Running')

    def _data_from_gen(self, gen):
        _raw_data_gen = self.logger.log_gen(gen)
        for raw_data in _raw_data_gen:
            self._raw_data = raw_data
            self.send_trigger()

    def buidl_buf_gen(self):
        self.buff_queque = multiprocessing.SimpleQueue()
        while True:
            #print("Wait for Signal")
            x = yield
            self._processor.process_raw_data(self._raw_data)
            # print('Plotting')
            render_process = multiprocessing.Process(target=self.build_process, args=(self,))
            render_process.start()
            render_process.join(timeout=self._max_render_timeout)
            render_process.terminate()
            self.buff = self.buff_queque.get()
            if render_process.exitcode is None:
                print('Aborted Rendering')

    def build_process(self, real_self):
        print('Started Rendering')
        buff = plot(data=real_self._processor.avg_processed_data(real_self.average_minutes), file=None)
        #time.sleep(self._max_render_timeout*2)
        self.buff_queque.put(buff)
        print('Finished Rendering')

    def build_buf(self):
        print('Creating Render-Gen')
        self.buff_gen = self.buidl_buf_gen()
        print('Created Render-Gen')
        next(self.buff_gen)
        print('Send Signal to Render-Gen')

    def change_settings(self, args: dict):
        changed = False
        if 'fill_in_minutes' in args.keys():
            if self._processor.fill_in_minutes != int(args['fill_in_minutes']):
                self._processor.fill_in_minutes = int(args['fill_in_minutes'])
                # print('fill_in_minutes Changed')
                changed = True
        if 'show_milliseconds' in args.keys():
            if self._processor.show_milliseconds != int(args['show_milliseconds']):
                self._processor.show_milliseconds = bool(args['show_milliseconds'])
                # print('show_milliseconds Changed')
                changed = True
        if 'max_minutes_ago' in args.keys():
            if self._processor.max_minutes_ago != int(args['max_minutes_ago']):
                # print('max_minutes_ago Changed', self._processor.max_minutes_ago , int(args['max_minutes_ago']))
                self._processor.max_minutes_ago = int(args['max_minutes_ago'])
                changed = True
        if 'average_minutes' in args.keys():
            if self.average_minutes != int(args['average_minutes']):
                self.average_minutes = int(args['average_minutes'])
                # print('average_minutes Changed')
                changed = True

        if changed:
            print('Args Changed')
            self.send_trigger()

    def get_buff(self):
        return self.buff


class Handler(CGIHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)

    def do_GET(self):
        if self.path.startswith('/test.png'):
            args = {}
            print('Recieving Image-Call')

            print('Checking for Args')
            try:
                arg_list = self.path.split('?')[1].split('&')
                for arg_string in arg_list:
                    arg = arg_string.split('=')
                    args[arg[0]] = arg[1]
            except Exception:
                print('No Args')

            print('Getting Buffer')
            global show
            content: bytes = show.get_buff()
            show.change_settings(args)
            if content is None:
                self.send_response(404)
                return

            # Respond with the file contents.
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            try:
                self.wfile.write(content)
            except Exception:
                print("Broken-Pipe")
        else:
            self.path = '/web' + self.path
            super().do_GET()


def custom_formatter(x, pos):
    if x == 7 or x == 9:
        return ''
    return '{:.1f}'.format(x / 10)


def plot(data: dict, file, figsize=(10, 3)):
    labels = []
    values = []
    # print('Getting Data')
    for key in data.keys():
        date = parser.parse(key, dayfirst=True)
        labels.append(date)
        values.append(data[key] * 10)

    # print('Create Subplot')
    fig, ax = plt.subplots(figsize=figsize)
    # print('Edit Axis')
    ax.bar(labels, values, 1 / len(labels))
    ax.xaxis.set_major_locator(ticker.LinearLocator(30))
    ax.margins(x=0)
    ax.set_ylim(ymin=1, ymax=10)

    # print('Set Scale')
    ax.set_yscale("log")

    # print('Set Formatter')
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %Hh"))
    # ax.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax.yaxis.set_major_formatter(custom_formatter)
    ax.yaxis.set_minor_formatter(custom_formatter)

    # print('Set Label')
    ax.set(xlabel=str(len(labels)) + " Samples", ylabel='disconnected time\n/total time', title='Disconnection-Rate')
    # ax.set_xticks()
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    plt.tight_layout()

    # print('Export')
    if file is None:
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        return buf.getvalue()

    fig.savefig(file)
    plt.close(fig)
    return


def start():
    # print("Serving")
    server_object = HTTPServer(server_address=('', 8042), RequestHandlerClass=Handler)
    server_object.serve_forever()


if __name__ == '__main__':
    data_importer = DataProcessor()
    data_importer.read_file_raw('ping.log')

    logger = PingLogger()

    logger.data = data_importer.raw_data

    # print('Creating Plotter')
    show = Plotter(logger)
    start()
