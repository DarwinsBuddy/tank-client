from os import path, uname

_ROOT = path.abspath(path.dirname(__file__))


def get_data(relative_path):
    return path.join(_ROOT, 'data', relative_path)


def is_raspberry():
    (sysname, nodename, release, version, machine) = uname()
    return sysname == 'Linux' and machine == 'armv6l'
