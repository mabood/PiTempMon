from utils import *
from PlotDataWindow import PlotDataWindow

class StatReporter:
    def __init__(self, WeatherStats, SensorReader, report_file):
        self.weather = WeatherStats
        self.sensor = SensorReader
        self.report_file = report_file
        self.touch_report_file()
        self.plot = PlotDataWindow()

    def touch_report_file(self):
        try:
            open(self.report_file, 'a')

        except IOError as e:
            logging.error('Unable to create report file: %s. \n%s' % (self.report_file, e.message))

    def update_temps_log(self, timestamp, sensor_temp_f, weather_temp_f):

        report = timestamp + ',' + str(sensor_temp_f) + ',' + str(weather_temp_f)

        try:
            fd = open(self.report_file, 'a')
            fd.write(report + '\n')

        except IOError as e:
            logging.error('Unable to write report file: %s. \n%s' % (self.report_file, e.message))

    def update_plot_data(self):
        timestamp = self.sensor.latest_measurement_time
        sensor_temp_f = self.sensor.latest_temp_f

        self.plot.read_latest_report()
        self.plot.write_all_datasets()
        self.plot.write_current_temps(timestamp, sensor_temp_f, self.weather)
        self.plot.write_daily_averages()

