from netmiko.huawei import HuaweiSSH
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import SSHException
from netmiko.exceptions import NetmikoTimeoutException
from asgiref.sync import sync_to_async


def run_command_list(ip, username, password, com_list):
    try:
        ne = HuaweiSSH(ip, username=username, password=password)
        if not(ne is None):
            promt = ne.find_prompt()[1:-1]
            yield {'status': f'Connected to {promt}'}
            for com in com_list:
                yield { 
                    'command': com,
                    'output': ne.send_command(com)
                }
    except (NetmikoAuthenticationException, SSHException, NetmikoTimeoutException):
        raise ConnectionError(f'Failed connect to {ip}')
        