# Software 
# display version, 
# display startup, 
# display patch-information

import sys
from os.path import dirname, abspath, join
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)
from output.output import log_commission


def check(acc_ne, ip):
    display_version(acc_ne, ip)
    display_startup(acc_ne, ip)
    display_patch_information(acc_ne, ip)
    

def display_version(acc_ne, ip):
    command = "display version"
    clear_output = '' 
    output = acc_ne.send_command(command)
    for line in output.split("\n"):
        if "software" in line or "uptime" in line:
            clear_output += f"{line} \n"
    result = "OK" if clear_output else "FAIL"
    log_commission(ip, command, result, output)


def display_startup(acc_ne, ip):
    command = "display startup"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "OK" #for test
    log_commission(ip, command, result, output)


def display_patch_information(acc_ne, ip):
    command = "display patch-information"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "OK" #for test
    log_commission(ip, command, result, output)
    
    