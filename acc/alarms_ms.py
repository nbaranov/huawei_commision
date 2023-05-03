#display alarm active / urgent, 
# dis alarm history, 
# display reboot-info, 
# ping 10.188.32.5, 
# ping 10.188.32.11


import sys
from os.path import dirname, abspath, join
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)
from output.output import log_commission

def check(acc_ne, ip):
    display_alarm_urgent(acc_ne, ip)
    display_reboot_info(acc_ne, ip)
    ping_ms1(acc_ne, ip)
    ping_ms2(acc_ne, ip)
    

def display_alarm_urgent(acc_ne, ip):
    command = "display alarm urgent"
    output = acc_ne.send_command(command)
    result = "OK" if len(output.split("\n")) < 4 else "FAIL"
    
    log_commission(ip, command, result, output)

# нет такой команды
# def display_alarm_history(acc_ne):
#     command = "display alarm history"
#     output = acc_ne.send_command(command)
#     # TODO parsing and checking
#     result = "OK" #for test
#     return command, result, output    


def display_reboot_info(acc_ne, ip):
    command = "display reboot-info"
    output = acc_ne.send_command(command)
    output = "\n".join(output.split("\n")[:8])
    result = "OK" # TODO check time last reboot

    log_commission(ip, command, result, output)


def ping_ms1(acc_ne, ip):
    command = "ping 10.188.32.5"
    output = acc_ne.send_command(command)
    result = "OK" if "0.00% packet loss" in output else "FAIL"
    log_commission(ip, command, result, output)


def ping_ms2(acc_ne, ip):
    command = "ping 10.188.32.11"
    output = acc_ne.send_command(command)
    result = "OK" if "0.00% packet loss" in output else "FAIL"
    log_commission(ip, command, result, output)
