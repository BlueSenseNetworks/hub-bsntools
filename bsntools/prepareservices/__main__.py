from subprocess import call
import argparse


def main():
    units = [
        {
            'unit': 'docker.service',
            'startable': True,
            'restart': False
        },
        {
            'unit': 'bsnd.service',
            'startable': True,
            'restart': True
        },
        {
            'unit': 'bsn-firstboot.service',
            'startable': False,
            'restart': False
        },
        {
            'unit': 'bsntools-autoupdate.service',
            'startable': False,
            'restart': False
        },
        {
            'unit': 'bsntools-autoupdate.timer',
            'startable': True,
            'restart': False
        },
        {
            'unit': 'bsnd-config-watch.path',
            'startable': True,
            'restart': False
        },
        {
            'unit': 'bluetooth-auto-power@hci0.service',
            'startable': True,
            'restart': False
        },
        {
            'unit': 'bluetooth-auto-power@hci1.service',
            'startable': True,
            'restart': False
        },
        {
            'unit': 'restart-wpa_supplicant@wlan0.path',
            'startable': True,
            'restart': False
        },
        {
            'unit': 'restart-wpa_supplicant@wlan0.service',
            'startable': False,
            'restart': False
        },
        {
            'unit': 'wpa_supplicant@wlan0.service',
            'startable': True,
            'restart': False
        },
        {
            'unit': 'bsn-status-page.service',
            'startable': True,
            'restart': True
        }
    ]

    parser = argparse.ArgumentParser(description='Enable and start required systemd units')

    parser.add_argument('--start', action='store_true', help='whether or not to start the required units')

    args = parser.parse_args()

    for unit in units:
        call('sudo systemctl enable ' + unit['unit'], shell=True)

        if unit['startable'] and args.start:
            if unit['restart']:
                call('sudo systemctl restart ' + unit['unit'], shell=True)
            else:
                call('sudo systemctl start ' + unit['unit'], shell=True)


if __name__ == "__main__":
    main()
