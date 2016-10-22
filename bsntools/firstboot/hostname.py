import re
import logging
from subprocess import check_output
import ConfigParser


def check_hostname():
    config = ConfigParser.ConfigParser()
    config.read('/etc/bsn/bsn.ini')
    hostname_prefix = config.get('Hostname', 'prefix')

    hosts_file_path = '/etc/hosts'
    current_host_name = check_output('hostname')
    regex = re.compile("^((?:\d{1,3}\.){3}\d{1,3})(\s+)(" + current_host_name + ")$", re.MULTILINE)

    serial = file('/proc/cpuinfo').read().split('Serial')[1].strip()[-8:]  # Get last 8 characters of the serial
    new_host_name = hostname_prefix + '-' + serial

    if new_host_name != current_host_name:
        logging.debug('Hostname mismatch, fixing...')

        # Change hostname in /etc/hostname
        logging.debug('Hostnamectl out: ' + check_output(['hostnamectl', 'set-hostname', new_host_name]))

        # Replace hostname in /etc/hosts
        hosts_file = file(hosts_file_path).read()
        hosts_file = (re.sub(regex, r"\1\2" + new_host_name, hosts_file))
        file(hosts_file_path, 'w').write(hosts_file)

