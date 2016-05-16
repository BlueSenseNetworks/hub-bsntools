import json
import logging
from subprocess import CalledProcessError
import semver
from docker import Docker


class NodeHub:
    """
    A class to abstract the application info
    """

    instance_name = 'bsn-node-hub'

    def __init__(self, branch, update_type, repository):
        self.branch = branch
        self.update_type = update_type
        self.repository = repository

    @staticmethod
    def stop_running_container():
        try:
            logging.debug('Stopping running container')
            Docker.stop(NodeHub.instance_name)
        except Exception, e:
            # possible cause includes container doesnt exist
            logging.warn('Stopping running container failed: ' + str(e))

    @staticmethod
    def remove_existing_container():
        try:
            logging.debug('Removing old container')
            Docker.rm(NodeHub.instance_name)
        except Exception, e:
            # possible cause includes container doesnt exist
            logging.warn('Removing old container failed: ' + str(e))

    @staticmethod
    def installed_application_image():
        try:
            image_info = json.loads(Docker.inspect(NodeHub.instance_name))[0]

            return {
                "version": image_info['Config']['Labels']['version'],
            }
        except:
            return False

    def application_images(self):
        return filter(lambda image: image['repository'] == self.repository, Docker.images())

    def remove_application_images_except(self, version):
        logging.debug('Removing all images except the new one')
        for image in self.application_images():
            if image['tag'] != version:
                logging.debug('Removing: ' + self.repository + ":" + image['tag'])
                Docker.rmi(self.repository + ":" + image['tag'])

    def get_wanted_version(self):
        installed_image = NodeHub.installed_application_image()

        if self.update_type == 'major' or not installed_image:
            version = 'latest'
        else:
            current_version = semver.parse(installed_image["version"])

            if self.update_type == 'minor':
                version = str(current_version['major'])
            else:
                version = str(current_version['major']) + '.' + str(current_version['minor'])

        if self.branch != 'production':
            version += '-' + self.branch

        return version

    def update(self):
        version = self.get_wanted_version()

        logging.debug('Fetching: ' + self.repository + ':' + version)
        try:
            out = Docker.pull(self.repository + ':' + version)
        except CalledProcessError, error:
            logging.error(error.output)
            return

        logging.debug('Docker pull output is: ' + out)

        if 'Status: Downloaded newer image for ' + self.repository + ':' + version in out:
            NodeHub.stop_running_container()
            NodeHub.remove_existing_container()
            self.remove_application_images_except(version)

            logging.debug('Running new version')
            self.start()
        else:
            logging.debug('No update found')

    def start(self):
        Docker.run([
                "-d",
                "--privileged",
                "--net=host",
                "--name=" + NodeHub.instance_name,
                "--restart=unless-stopped",
                "-v", "/var/log:/var/log",
                "-v", "/etc/wpa_supplicant:/etc/wpa_supplicant",
                self.repository + ":" + self.get_wanted_version()
            ])

    def start_if_not_running(self):
        try:
            json.loads(Docker.inspect(NodeHub.instance_name))
        except:
            self.start()
