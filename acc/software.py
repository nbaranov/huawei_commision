# Software 
# display version, 
# display startup, 
# display patch-information

from pprint import pprint
    

def display_version(acc_ne):
    command = "display version"
    clear_output = '' 
    output = acc_ne.send_command(command)
    for line in output.split("\n"):
        if "software" in line or "uptime" in line:
            clear_output += f"{line} \n"
    result = "OK" if clear_output else "FAIL"
    return command, result, clear_output


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
    
    