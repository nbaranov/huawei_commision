from netmiko.huawei import HuaweiSSH
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import SSHException
from netmiko.exceptions import NetmikoTimeoutException


def run_command_list(ip, username, password, com_list):
    try:
        ne = HuaweiSSH(ip, username=username, password=password)
        if not(ne is None):
            promt = ne.find_prompt()[1:-1]
            yield {'status': f'Connected to {promt}'}
            for com in com_list:
                output = ne.send_command(com.command)
                check_status = ''
                if com.check_include:
                    for string in com.check_include.split('\n'):
                        check_status = 'ok' if string in output else check_status
                if com.check_exclude:
                    for string in com.check_exclude.split('\n'):
                        check_status = 'false' if string in output else check_status
                if com.out_line_limit:
                    output = '\n'.join(output.split('\n')[:com.out_line_limit])
                yield { 
                    'command': com.command,
                    'check_status': check_status,
                    'output': output
                }
    except (NetmikoAuthenticationException, SSHException, NetmikoTimeoutException):
        raise ConnectionError(f'Failed connect to {ip}')
        