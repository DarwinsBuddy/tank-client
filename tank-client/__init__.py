import os


def is_raspberry():
    (sysname, nodename, release, version, machine) = os.uname()
    return sysname == 'Linux' and machine == 'armv6l'
