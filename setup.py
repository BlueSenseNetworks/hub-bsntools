from setuptools import setup

setup(
    # Application name:
    name="BsnDaemon",

    # Application author details:
    author="Nemanja Tosic",
    author_email="nemanja@bluesensenetworks.com",

    platforms=["arm"],

    # Packages
    packages=["bsntools", "bsntools.firstboot"],

    entry_points={
        'console_scripts': [
            'bsn-firstboot = bsntools.firstboot.__main__:main'
        ],
    }
)
