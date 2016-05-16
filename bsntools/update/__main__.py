import os
import logging
from nodehub import NodeHub
import argparse
import ConfigParser

log_directory = '/var/log/node-hub'
log_file = 'update.log'


def read_config():
    config = ConfigParser.ConfigParser()
    config.read('/etc/bsn/bsnd.ini')

    return {
        'update_interval': config.get('Update', 'Interval'),
        'update_level': config.get('Update', 'Level'),
        'update_stability': config.get('Update', 'Stability'),
        'update_repository': config.get('Update', 'Repository')
    }


def configure_logging():
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logging.basicConfig(format='%(asctime)s %(message)s', filename=log_directory + '/' + log_file, level=logging.DEBUG)


def update():
    config = read_config()
    parser = argparse.ArgumentParser(description='Update the BSN hub application')

    parser.add_argument('--branch',
                        default=config['update_stability'],
                        choices=['production', 'staging', 'dev'],
                        help='the branch to get updates from')
    parser.add_argument('--type',
                        default=config['update_level'],
                        choices=['major', 'minor', 'patch'],
                        help='the update type, semver.org spec')
    parser.add_argument('--repository',
                        default=config['update_repository'],
                        help='the repository from which to pull from')

    args = parser.parse_args()

    configure_logging()

    NodeHub(args.branch, args.type, args.repository).update()


def watchdog():
    config = read_config()

    NodeHub(config['update_stability'], config['update_level'], config['update_repository']).start_if_not_running()
