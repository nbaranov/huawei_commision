# display device, 
# display temperature all, 
# display cpu-usage, 
# display environment, 
# display elabel

import sys
from os.path import dirname, abspath, join
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)
from output.output import log_commission


def check(acc_ne, ip) -> None:
    display_device(acc_ne, ip)
    display_temperature_all(acc_ne, ip)
    display_cpu_usage(acc_ne, ip)
    display_environment(acc_ne, ip)
    display_elabel(acc_ne, ip)


def display_device(acc_ne, ip) -> None:
    command = "display device"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "OK" #for test
    log_commission(ip, command, result, output)    


def display_temperature_all(acc_ne, ip) -> None:
    command = "display temperature all"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "OK" #for test
    log_commission(ip, command, result, output)    


def display_cpu_usage(acc_ne, ip):
    command = "display cpu-usage"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "OK" #for test
    log_commission(ip, command, result, output)    


def display_environment(acc_ne, ip):
    command = "display environment"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "OK" #for test
    log_commission(ip, command, result, output)    


def display_elabel(acc_ne, ip):
    command = "display elabel"
    output = acc_ne.send_command(command)
    # TODO parsing and checking
    result = "OK" #for test
    log_commission(ip, command, result, output)    

