from setuptools import setup

setup(
    # Application name:
    name="BsnDaemon",

    # Application author details:
    author="Nemanja Tosic",
    author_email="nemanja@bluesensenetworks.com",

    platforms=["arm"],

    # Packages
    packages=["bsntools", "bsntools.daemon", "bsntools.firstboot", "bsntools.update", "bsntools.prepareservices"],

    entry_points={
        'console_scripts': [
            'bsnd = bsntools.daemon.__main__:main',
            'bsn-firstboot = bsntools.firstboot.__main__:main',
            'bsn-update = bsntools.update.__main__:update',
            'bsn-watchdog = bsntools.update.__main__:watchdog',
            'bsn-prepare-services = bsntools.prepareservices.__main__:main'
        ],
    }
)
