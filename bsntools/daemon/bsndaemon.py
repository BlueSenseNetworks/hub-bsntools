from time import sleep
from subprocess import check_output
import os
import logging
import ConfigParser


class BsnDaemon:
    log_directory = '/var/log/node-hub'
    log_file = 'daemon.log'
    config_file = '/etc/bsn/bsnd.ini'

    def __init__(self):
        pass

    @staticmethod
    def configure_logging():
        if not os.path.exists(BsnDaemon.log_directory):
            os.makedirs(BsnDaemon.log_directory)

        logging.basicConfig(format='%(asctime)s %(message)s',
                            filename=BsnDaemon.log_directory + '/' + BsnDaemon.log_file, level=logging.DEBUG)

    @staticmethod
    def run():
        BsnDaemon.configure_logging()

        config = ConfigParser.ConfigParser()
        config.read(BsnDaemon.config_file)
        update_interval = config.get('Update', 'interval')

        logging.debug('Started update daemon,  interval: ' + update_interval)
        while True:
            sleep(1)
