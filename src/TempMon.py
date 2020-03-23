
from utils import *
from StatReporter import StatReporter
import SensorReader
import IntervalTimer
import WeatherStats

def poll_and_write(sensor, weather, reporter):
    logging.info('Polling sensor...')
    sensor.poll_sensor_and_update()
    timestamp = sensor.latest_measurement_time
    sensor_temp_f = sensor.latest_temp_f
    weather_temp_f = weather.temp_f

    logging.info('Measured at: %s' % timestamp)
    logging.info('Sensor read: %fF' % sensor_temp_f)

    logging.info('Acquiring weather stats...')
    logging.info('Current temperature in %s: %fF' % (weather.city, weather_temp_f))

    logging.info('Updating temps log file: %s' % reporter.report_file)
    reporter.update_temps_log(timestamp, sensor_temp_f, weather_temp_f)

    logging.info('Updating data plots...')
    reporter.update_plot_data()

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

    # initialize StatReporter
    reporter = StatReporter(weather, sensor, report_file)

    # establish polling interval
    interval = int(get_property('POLLING_INTERVAL', 'SENSOR'))

    poll_and_write(sensor, weather, reporter)

    # Schedule interval job
    it = IntervalTimer.IntervalTimer(float(interval), poll_and_write, sensor, weather, reporter)

if __name__ == '__main__':
    main()