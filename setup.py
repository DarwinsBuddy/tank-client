from distutils.command.install import install

from setuptools import setup, find_packages

RESOURCES = "resources"
MODULE = "tank-client"


class InstallWrapper(install):
    def run(self):
        # now run install :)
        install.run(self)


setup(
    name=f'{MODULE}',
    author="Christoph Spörk",
    author_email="christoph.spoerk@gmail.com",
    platforms="any",
    version='0.1.0',
    packages=find_packages(
        include=[f'{MODULE}', f'{MODULE}.*']
    ),
    package_data={"tank-client": [
        "resources/tank-client.service"
    ]},
    cmdclass={
        'install': InstallWrapper,
    },
    install_requires=[
        'APScheduler==3.7.0',
        'pyzmq==22.2.1'
    ]
)
