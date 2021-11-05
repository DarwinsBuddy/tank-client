import os
import subprocess
import sys
from distutils.command.install import install

from setuptools import setup, find_packages

deps = [
    'APScheduler==3.7.0',
    'pyzmq==22.2.1'
]


def is_raspberry():
    (sysname, nodename, release, version, machine) = os.uname()
    return sysname == 'Linux' and machine == 'armv6l'


MODULE = "tank-client"


class InstallWrapper(install):

    @staticmethod
    def pip_install(package_name):
        subprocess.call(
            [sys.executable, '-m', 'pip', 'install', package_name]
        )

    def run(self):
        # install all deps
        for dep in deps:
            self.pip_install(dep)
        if is_raspberry():
            self.pip_install('RPi.GPIO==0.7.0')
        # now run install :)
        install.run(self)


setup(
    name=f'{MODULE}',
    author="Christoph Spörk",
    author_email="christoph.spoerk@gmail.com",
    platforms="any",
    version='1.1.0',
    packages=find_packages(
        include=[
            f'{MODULE}', f'{MODULE}.*'
        ]
    ),
    package_data={"tank-client": [
        "data/tank-client.service",
        "data/tank-client.conf"
    ]},
    cmdclass={
        'install': InstallWrapper,
    },
    install_requires=deps
)
