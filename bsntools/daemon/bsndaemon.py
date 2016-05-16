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
        elapsed = 0

        logging.debug('Started update daemon,  interval: ' + update_interval)
        while True:
            if elapsed % 300 == 0:
                check_output(['bsn-watchdog'])

            if elapsed % int(update_interval) == 0:
                try:
                    check_output(['bsn-update'])
                    check_output('docker images --quiet --filter=dangling=true | xargs --no-run-if-empty docker rmi',
                                 shell=True)
                except Exception, e:
                    logging.error('Exception: ' + str(e))

            elapsed += 1
            sleep(1)
