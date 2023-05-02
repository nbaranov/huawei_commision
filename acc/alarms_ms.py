#display alarm active / urgebt, 
# dis alarm history, 
# display reboot-info, 
# ping 10.188.32.5, 
# ping 10.188.32.11


from pprint import pprint
    

def display_alarm_urgent(acc_ne):
    command = "display alarm urgent"
    output = acc_ne.send_command(command)
    print(output)
    result = "OK" if len(output.split("\n")) < 4 else "FAIL"
    return command, result, output

# нет такой команды
# def display_alarm_history(acc_ne):
#     command = "display alarm history"
#     output = acc_ne.send_command(command)
#     # TODO parsing and checking
#     result = "OK" #for test
#     return command, result, output    


def display_reboot_info(acc_ne):
    command = "display reboot-info"
    output = acc_ne.send_command(command)
    output = "\n".join(output.split("\n")[:8])
    result = "OK" # TODO check time last reboot

    return command, result, output


def ping_ms1(acc_ne):
    command = "ping 10.188.32.5"
    output = acc_ne.send_command(command)
    result = "OK" if "0.00% packet loss" in output else "FAIL"
    return command, result, output


def ping_ms2(acc_ne):
    command = "ping 10.188.32.11"
    output = acc_ne.send_command(command)
    result = "OK" if "0.00% packet loss" in output else "FAIL"
    return command, result, output
