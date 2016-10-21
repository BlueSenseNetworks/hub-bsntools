import logging
from subprocess import check_output


def setup():
    hostname = check_output('hostname').strip()
    certname =  hostname + '.nodes.bluesense.co'
    logging.debug('puppet agent certname will be set to: ' + certname)

    puppet_config_file_path = '/etc/puppetlabs/puppet/puppet.conf'
    puppet_config = '[main]\n' \
                    'server = puppet-fleet.bluesense.co\n' \
                    '[agent]\n' \
                    'certname = ' + certname + '\n'

    file(puppet_config_file_path, 'w').write(puppet_config)

    check_output(['systemctl', 'enable', 'puppet'])
    check_output(['systemctl', 'start', 'puppet'])

