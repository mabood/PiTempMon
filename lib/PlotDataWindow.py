# -*- coding: utf-8 -*-

from utils import *
from os import listdir
from os.path import isfile, join
import datetime
import json
import time

class PlotDataWindow():
    def __init__(self):
        self.report_dir = get_property('REPORT_DIR', 'CONFIG')
        self.report_suffix = get_property('REPORT_FILE', 'CONFIG')
        self.file_time_format = get_property('FILE_TIME', 'CONFIG')
        self.timestamp_format = get_property('TIME_FORMAT', 'CONFIG')
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
        self.avgs = get_property('AVGS', 'PLOTS')

        self.num_data_points = int(get_property('PLOT_POINTS', 'PLOTS'))
        self.max_hticks = int(get_property('MAX_HTICKS', 'PLOTS'))
        self.max_vticks = 12
        self.day_seconds = 86400

    def convert_utc(self, timestamp):
        basetime = datetime.datetime.strptime(timestamp, self.timestamp_format)
        converted = basetime.strftime(self.timestamp_format) + time.strftime("%z")
        return converted

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
        window = self.day_seconds / 2
        points = self.extract_data_window(window)
        hticks = self.generate_hticks(points, window)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_12 + '.json', points, hticks, vticks)

    def generate_24hr_dataset(self):
        window = self.day_seconds
        points = self.extract_data_window(window)
        hticks = self.generate_hticks(points, window)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_24 + '.json', points, hticks, vticks)

    def generate_2d_dataset(self):
        window = self.day_seconds * 2
        points = self.extract_data_window(window)
        hticks = self.generate_hticks(points, window)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_2d + '.json', points, hticks, vticks)

    def generate_5d_dataset(self):
        window = self.day_seconds * 5
        points = self.extract_data_window(window)
        hticks = self.generate_hticks(points, window)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_5d + '.json', points, hticks, vticks)

    def generate_10d_dataset(self):
        window = self.day_seconds * 5
        points = self.extract_data_window(window)
        hticks = self.generate_hticks(points, window)
        vticks = self.generate_vticks(points)
        self.write_window_data(self.plot_10d + '.json', points, hticks, vticks)

    def generate_hticks(self, points, window):
        if len(points) < 1:
            return None

        ceil_time = datetime.datetime.strptime(points[len(points) - 1][0], self.timestamp_format)
        floor_time = ceil_time - datetime.timedelta(seconds=window)
        hours = datetime.timedelta(seconds=window).total_seconds() / 3600
        tick_gap = 1
        while int((hours / tick_gap)) > self.max_hticks:
            tick_gap += 1

        hticks = [floor_time]
        for i in range(1, int(hours / tick_gap) - 1):
            hticks.append(floor_time + datetime.timedelta(seconds=(3600 * tick_gap * i)))

        return hticks

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
        possible_data_points = window / data_interval

        if len(self.full_report) > possible_data_points:
            sig_points = self.full_report[len(self.full_report) - 1 - possible_data_points:]
        else:
            sig_points = self.full_report

        point_gap = int(possible_data_points / self.num_data_points)
        if point_gap < 1:
            point_gap = 1

        plot_list = []
        counter = point_gap - (len(sig_points) - 1) % point_gap
        for tup in sig_points:
            if counter % point_gap is 0:
                cols = tup.split(',')
                tm = cols[0]
                plot_list.append([tm, cols[1], cols[2]])

            counter += 1

        return plot_list

    def write_window_data(self, filename, points, hticks, vticks):
        # first convert times to UTC
        utc_points = list()
        for point in points:
            utc_points.append([self.convert_utc(point[0]), point[1], point[2]])

        data = {
            'hticks':hticks,
            'vticks':vticks,
            'dataset':utc_points
        }

        with open(self.plot_dir + filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info('Wrote %d points to file: %s' % (len(points), filename))

    def write_current_temps(self, timestamp, s_temp, weather):
        w_temp = weather.temp_f
        w_location = weather.city
        data = {
            'timestamp': self.convert_utc(timestamp),
            'sensor': {'temp_f': s_temp},
            'weather': {'temp_f': w_temp, 'location': w_location}
        }
        with open(self.plot_dir + self.current + '.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def write_daily_averages(self):
        days = dict()
        avgs = dict()
        for tup in self.full_report:
            cols = tup.split(',')
            day = cols[0].split('T')[0]
            s_temp = cols[1]
            w_temp = cols[2]
            if days.has_key(day):
                days[day].append({'timestamp':cols[0], 's_temp':s_temp, 'w_temp':w_temp})
            else:
                days[day] = []

        for day in days:
            times = []
            s_temps = []
            w_temps = []

            for point in days[day]:
                times.append(datetime.datetime.strptime(point['timestamp'], self.timestamp_format))
                s_temps.append(point['s_temp'])
                w_temps.append(point['w_temp'])

            avgs[day] = {
                'time_start': self.convert_utc(min(times).strftime(self.timestamp_format)),
                'time_end': self.convert_utc(max(times).strftime(self.timestamp_format)),
                's_avg': sum(s_temps) / len(s_temps),
                'w_avg': sum(w_temps) / len(w_temps)
            }

        with open(self.plot_dir + self.avgs + '.json', 'w') as json_file:
            json.dump(avgs, json_file, indent=4)
