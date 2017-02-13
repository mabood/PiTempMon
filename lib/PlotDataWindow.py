from utils import *
from os import listdir
from os.path import isfile, join
import datetime
import json

class PlotDataWindow():
    def __init__(self):
        self.report_dir = get_property('REPORT_DIR', 'CONFIG')
        self.report_suffix = get_property('REPORT_FILE', 'CONFIG')
        self.file_time_format = get_property('FILE_TIME', 'CONFIG')
        self.latest_report = self.get_latest_report()
        self.full_report = self.read_report(self.latest_report)

        self.plot_dir = get_property('PLOT_DATA_DIR', 'CONFIG')

    def get_latest_report(self):
        reports = [f for f in listdir(self.report_dir) if isfile(join(self.report_dir, f))]
        tail = '-' + self.report_suffix
        dates = map(lambda x: datetime.datetime.strptime(x[0: x.index(tail)], self.file_time_format), reports)
        dates.sort(reverse=True)
        return dates[0].strftime(self.file_time_format) + tail

    def read_report(self, report_file):
        try:
            fd = open(self.report_dir + report_file)
            return fd.readlines()
        except:
            logging.error('Unable to read report file: %s' % report_file)

    def generate_12hr_dataset(self):
        #generate 12 ticks
        last_tuple = self.full_report[len(self.full_report) - 1]
        last_hour = int(last_tuple.split(',')[0].split(':')[0].split('T')[1])
        ticks = [last_hour]
        for i in range(1, 12):
            tick = last_hour - i
            if tick < 0:
                tick += 24
            ticks.append(tick)
        ticks.sort(reverse=True)
        ticks = map(lambda x: str(x) + ':00', ticks)

        self.write_window_data(get_property('PLOT_12', 'CONFIG') + '.json', 43200, ticks)

    def generate_24hr_dataset(self):
        # generate 12 ticks
        last_tuple = self.full_report[len(self.full_report) - 1]
        last_hour = int(last_tuple.split(',')[0].split(':')[0].split('T')[1])
        ticks = [last_hour]
        for i in range(1, 12):
            tick = last_hour - (i * 2)
            if tick < 0:
                tick += 24
            ticks.append(tick)
        ticks.sort(reverse=True)
        ticks = map(lambda x: str(x) + ':00', ticks)

        self.write_window_data(get_property('PLOT_24', 'CONFIG') + '.json', 86400, ticks)

    def write_window_data(self, filename, window_seconds, ticks):
        # fun math
        data_interval = int(get_property('POLLING_INTERVAL', 'SENSOR'))
        total_data_points = window_seconds / data_interval

        # 360 data points
        if len(self.full_report) > total_data_points:
            sig_points = total_data_points[len(self.full_report) - total_data_points:]
        else:
            sig_points = self.full_report

        point_gap = int(total_data_points / 360)
        if point_gap < 1:
            point_gap = 1

        plot_list = []
        counter = 1
        for tuple in sig_points:
            if counter is point_gap:
                cols = tuple.split(',')
                tm = cols[0].split('T')[1]
                plot_list.append([tm, cols[1], cols[2]])
                counter = 1
            else:
                counter += 1

        data = {
            'ticks':ticks,
            'dataset':plot_list
        }

        with open(self.plot_dir + filename, 'w') as json_file:
            json.dump(data, json_file)
