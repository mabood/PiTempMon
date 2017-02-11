from utils import *
import SensorReader
import time

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

    # establish report file
    report_file = get_property('REPORT_DIR', 'CONFIG')
    report_file += get_property('REPORT_FILE', 'CONFIG')

    # establish polling interval
    interval = get_property('POLLING_INTERVAL', 'SENSOR')

    while True:
        logging.info('Polling sensor...')
        (timestamp, temp_c) = sensor.measure_temp()
        temp_f = sensor.convert_c_to_f(temp_c)

        logging.info('Sensor read: %dC, %dF' % temp_c, temp_f)

        logging.info('Writing to file: %s...' % report_file)
        sensor.report_to_file(timestamp, temp_f, report_file)

        time.sleep(interval)

if __name__ == '__main__':
    main()