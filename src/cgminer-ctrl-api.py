#!/usr/bin/python

#format of command entry:
# command : is privleged?, args, description


def api_commands_1_28():
    return { "version" : (False, (), "cgminer version info"),
             "config" : (False, (), "cgminer config info"),
             "summary" : (False, (), "cgminer status summary"),
             "pools" : (False, (), "status of each pool"),
             "devs" : (False, (), "details of attached devices"),
             "gpu" : (False, ('N'), "details of GPU N"),
             "pga" : (False, ('N'), "details of (F)PGA N")
             "gpucount" : (False, (), "number of GPUs"),
             "pgacount" : (False, (), "number of (F)PGAs"),
             "switchpool" : (True, ('N'), "enable/make pool N highest priority"),
             "enablepool" : (True, ('N'), "enable pool N"),
             "addpool" : (True, ('URL','USR','PASS'), "add pool at given url"),
             "poolpriority" : (True, ('N','*special'), "change pool N priority"),
             "disablepool" : (True, ('N'), "disable pool N"),
             "removepool" : (True, ('N'), "remove pool N"),
             "save" : (True, (filename))
             }

def api_commands_1_29():
    return api_commands_1_28()

def api_commands(majver, minver):
    if majver <= 1:
        if minver <= 28:
            return ((1, 28), api_commands_1_28())
        if minver >= 29:
            return ((1, 29), api_commands_1_29())

    return ((1, 29), api_commands_1_29())
