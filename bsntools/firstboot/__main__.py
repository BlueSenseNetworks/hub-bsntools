import os
import logging
import resizedisk
import hostname
import puppet


def main():
    log_path = '/var/log/node-hub'
    log_file = 'firstboot.log'

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    logging.basicConfig(format='%(asctime)s %(message)s', filename=log_path + '/' + log_file, level=logging.DEBUG)

    logging.debug('Set hostname')
    hostname.check_hostname()

    logging.debug('Resize disk')
    resizedisk.resize()

    logging.debug('Set up puppet')
    puppet.setup()

if __name__ == "__main__":
    main()

