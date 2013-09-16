#!/usr/bin/python

class values:
    install_path = '/home/pi/src/stripmine/src'

    local_config = install_path + '/etc/stripmine_local.conf'


def values_dict():
    allnames = [attr for attr in dir(values()) if not callable(getattr(values(),attr)) and not attr.startswith("__")]

    ret = {}
    for name in allnames:
        ret[name] = getattr(values(),name)

    return ret

if __name__ == "__main__":
    vals = values_dict()
    for key,val in vals:
        print key, ":", val
