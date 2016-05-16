import subprocess
import re
from subprocess import STDOUT


class Docker:
    def __init__(self):
        pass

    @staticmethod
    def images():

        def extract_info(line):
            info = re.sub('\s\s+', ' ', line).split(' ')
            return {
                "repository": info[0],
                "tag": info[1]
            }

        images = subprocess.check_output(["docker", "images"]).split('\n')[1:]
        # remove header
        images.pop()

        return map(extract_info, images)

    @staticmethod
    def containers():
        def extract_info(line):
            info = line.strip().split(' ')
            return {
                "id": info[1],
                "name": info[0][1:],
                "image": info[2]
            }

        # get ids
        containers = subprocess.check_output(["docker", "ps", "-a", "-q"]).split('\n')[:-1]

        # format
        containers = map(lambda container_id: subprocess.check_output(["docker", "inspect", "--format='{{.Name}} {{.Id}} {{.Image}}'", container_id]), containers)

        return map(extract_info, containers)

    @staticmethod
    def pull(image):
        return subprocess.check_output(["docker", "pull", image], stderr=STDOUT)

    @staticmethod
    def run(params):
        return subprocess.check_output(["docker", "run"] + params)

    @staticmethod
    def stop(id):
        return subprocess.check_output(["docker", "stop", id])

    @staticmethod
    def rm(id):
        return subprocess.check_output(["docker", "rm", id])

    @staticmethod
    def rmi(id):
        return subprocess.check_output(["docker", "rmi", id])

    @staticmethod
    def inspect(id):
        return subprocess.check_output(["docker", "inspect", id])
