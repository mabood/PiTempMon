
from utils import *
from PlotDataWindow import PlotDataWindow
import SensorReader
import IntervalTimer
import WeatherStats

def poll_and_write(sensor, weather, report_file, plot=None):
    logging.info('Polling sensor...')
    (timestamp, temp_c) = sensor.measure_temp()

    temp_f = sensor.convert_c_to_f(temp_c)
    logging.info('Sensor read: %fC, %fF' % (temp_c, temp_f))

    logging.info('Requesting weather stats...')
    logging.info('Current temperature in %s: %sF' % (weather.city, str(weather.temp_f)))

    logging.info('Writing report to file: %s...' % report_file)
    sensor.report_to_file(timestamp, temp_f, report_file, weather.temp_f)

    if plot:
        logging.info('Generating data plots...')
        plot.read_report()
        plot.generate_12hr_dataset()
        plot.generate_24hr_dataset()
        plot.write_current_temps(timestamp, temp_f, weather.temp_f)

def main():
    # setup
    setup_logger()
    log_title('TEMPMON')
    check_files()

    device_name = get_property('DEVICE_NAME', 'SENSOR')
    logging.info('Checking device directory...')

    if device_exists():
        logging.info('Device: %s found!' % device_name)
    else:
        logging.critical('Cannot locate device: %s' % device_name)
        report_failed_and_exit('No sensor found')

    # initialize sensor reader
    sensor = SensorReader.SensorReader()

    # initialize WeatherStats object
    weather = WeatherStats.WeatherStats()

    # establish report file
    report_file = get_property('REPORT_DIR', 'CONFIG')
    report_file += generate_filetime() + '-'
    report_file += get_property('REPORT_FILE', 'CONFIG')

    # establish polling interval
    interval = int(get_property('POLLING_INTERVAL', 'SENSOR'))

    poll_and_write(sensor, weather, report_file)

    # initialize WindowPlotter
    plot = PlotDataWindow()

    # Schedule interval job
    it = IntervalTimer.IntervalTimer(float(interval), poll_and_write, sensor, weather, report_file, plot)


if __name__ == '__main__':
    main()