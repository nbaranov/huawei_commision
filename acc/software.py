# Software (display version, display startup, display patch-information)
from pprint import pprint
    

def display_version(acc_ne):
    command = "display version"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "FAIL" #for test
    return command, result, output

    
def display_startup(acc_ne):
    command = "display startup"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "OK" #for test
    return command, result, output    

def display_patch_information(acc_ne):
    command = "display patch-information"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "OK" #for test
    return command, result, output
    
    