# -*- coding: utf-8 -*-

from utils import *
from os import listdir
from os.path import isfile, join
import datetime
import json
import math

class PlotDataWindow():
    def __init__(self):
        self.report_dir = get_property('REPORT_DIR', 'CONFIG')
        self.report_suffix = get_property('REPORT_FILE', 'CONFIG')
        self.file_time_format = get_property('FILE_TIME', 'CONFIG')
        self.latest_report = self.get_latest_report()
        self.full_report = self.read_report(self.latest_report)
        self.poll_interval = int(get_property('POLLING_INTERVAL', 'SENSOR'))

        self.plot_dir = get_property('PLOT_DATA_DIR', 'PLOTS')
        self.plot_12 = get_property('PLOT_12', 'PLOTS')
        self.plot_24 = get_property('PLOT_24', 'PLOTS')
        self.plot_2d = get_property('PLOT_2d', 'PLOTS')
        self.plot_5d = get_property('PLOT_5d', 'PLOTS')
        self.plot_10d = get_property('PLOT_10d', 'PLOTS')
        self.current = get_property('CURRENT', 'PLOTS')

        self.num_data_points = int(get_property('PLOT_POINTS', 'PLOTS'))
        self.max_hticks = int(get_property('MAX_HTICKS', 'PLOTS'))
        self.max_vticks = 12
        self.day_seconds = 86400

    def get_latest_report(self):
        reports = [f for f in listdir(self.report_dir) if isfile(join(self.report_dir, f))]
        tail = '-' + self.report_suffix
        dates = map(lambda x: datetime.datetime.strptime(x[0: x.index(tail)], self.file_time_format), reports)
        dates.sort(reverse=True)
        return dates[0].strftime(self.file_time_format) + tail

    def read_report(self, report_file):
        lines = []
        try:
            fd = open(self.report_dir + report_file)
            lines = map(lambda x: x.strip('\n'), fd.readlines())
            fd.close()
        except:
            logging.error('Unable to read report file: %s' % report_file)

        return lines

    def read_latest_report(self):
        self.latest_report = self.get_latest_report()
        self.full_report = self.read_report(self.latest_report)

    def write_all_datasets(self):
        self.generate_12hr_dataset()
        self.generate_24hr_dataset()
        self.generate_2d_dataset()
        self.generate_5d_dataset()
        self.generate_10d_dataset()

    def generate_12hr_dataset(self):
        points = self.extract_data_window(self.day_seconds / 2)
        hticks = self.generate_hticks(points)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_12 + '.json', points, hticks, vticks)

    def generate_24hr_dataset(self):
        points = self.extract_data_window(self.day_seconds)
        hticks = self.generate_hticks(points)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_24 + '.json', points, hticks, vticks)

    def generate_2d_dataset(self):
        points = self.extract_data_window(self.day_seconds * 2)
        hticks = self.generate_hticks(points)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_2d + '.json', points, hticks, vticks)

    def generate_5d_dataset(self):
        points = self.extract_data_window(self.day_seconds * 5)
        hticks = self.generate_hticks(points)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_5d + '.json', points, hticks, vticks)

    def generate_10d_dataset(self):
        points = self.extract_data_window(self.day_seconds * 10)
        hticks = self.generate_hticks(points)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_10d + '.json', points, hticks, vticks)

    def generate_hticks(self, points):
        if len(points) < 1:
            return None

        #floor_time = datetime.datetime.strptime(points[0][0], '%H:%M:%S')
        #ceil_time = datetime.datetime.strptime(points[len(points) - 1][0], '%H:%M:%S')



    def generate_vticks(self, points):

        if len(points) < 2:
            return None

        all_points = []
        vals = []

        for point in points:
            all_points.append(float(point[1]))
            all_points.append(float(point[2]))

        max_point = max(all_points)
        min_point = min(all_points)
        std_dev = max_point - min_point

        div = std_dev / 10.0
        if div < 0.1:
            # ticks < 0.1 apart -> become 0.1 intervals
            vals = self.generate_ticks_on_range(min_point, max_point, 0.1)

        elif div < 0.2:
            #ticks < 0.2 apart -> become 0.2 intervals
            vals = self.generate_ticks_on_range(min_point, max_point, 0.2)

        elif div < 0.25:
            #ticks < 0.2 apart -> become 0.2 intervals
            vals = self.generate_ticks_on_range(min_point, max_point, 0.25)

        elif div < 0.5:
            #ticks < 0.5 apart -> become 0.5 intervals
            vals = self.generate_ticks_on_range(min_point, max_point, 0.5)

        elif div < 1:
            #ticks < 1 apart -> become 1 intervals
            vals = self.generate_ticks_on_range(min_point, max_point, 1)

        elif div < 2:
            #ticks < 2 apart -> become 2 intervals
            vals = self.generate_ticks_on_range(min_point, max_point, 2)

        elif div < 5:
            #ticks < 5 apart -> bcome 5 intervals
            vals = self.generate_ticks_on_range(min_point, max_point, 5)

        elif div < 10:
            #ticks < 10 apart -> bcome 10 intervals
            vals = self.generate_ticks_on_range(min_point, max_point, 10)

        return self.format_ticks(map(lambda a: (a, str(a)), vals))

    def generate_ticks_on_range(self, low, high, difference):
        floor = low - (low % difference)
        ceiling = high - (high % difference) + difference
        num_ticks = int((ceiling - floor) / difference + 1)

        vals = [floor]
        for i in range(1, num_ticks):
            vals.append(floor + (difference * i))

        return vals

    def format_ticks(self, vf_pairs):
        ticks = []

        for pair in vf_pairs:
            ticks.append({'v': pair[0], 'f': pair[1]})

        return ticks


    def extract_data_window(self, window):
        # fun math
        data_interval = self.poll_interval
        total_data_points = window / data_interval

        # 120 data points
        if len(self.full_report) > total_data_points:
            sig_points = self.full_report[len(self.full_report) - total_data_points:]
        else:
            sig_points = self.full_report

        point_gap = int(total_data_points / self.num_data_points)
        if point_gap < 1:
            point_gap = 1

        plot_list = []
        counter = len(sig_points) % point_gap
        for tup in sig_points:
            if counter % point_gap is 0:
                cols = tup.split(',')
                tm = cols[0].split('T')[1]
                tm = tm[:-3]
                plot_list.append([tm, cols[1], cols[2]])

            counter += 1

        return plot_list

    def write_window_data(self, filename, points, hticks, vticks):


        data = {
            'hticks':hticks,
            'vticks':vticks,
            'dataset':points
        }

        with open(self.plot_dir + filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info('Wrote %d points to file: %s' % (len(points), filename))

    def write_current_temps(self, timestamp, s_temp, weather):
        w_temp = weather.temp_f
        w_location = weather.city
        data = {
            'timestamp':timestamp,
            'sensor': {'temp_f': s_temp},
            'weather': {'temp_f': w_temp, 'location': w_location}
        }
        with open(self.plot_dir + self.current + '.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def write_daily_averages(self):
        pass