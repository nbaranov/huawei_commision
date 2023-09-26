
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import SSHException
from netmiko.exceptions import NetmikoTimeoutException
from re import search

import asyncio
from asgiref.sync import sync_to_async

from n3com.n3com import N3ComSSH
from commision.models import AutonomicSystem


def choose_func(command):
    match command:
        # case 'command':
        #    return functions name
        case _:
            return default_command_func


# async def dis_cur_configuration_bgp(ne, com, ip, agg_ip):
#     status = 'ok'
#     comment = ''
#     output = ne.send_command(com.command)
#     out_for_check = output.split('#')
#     # check exist configuration
#     bgp_cfg = [block.strip() for block in out_for_check if block.strip().startswith('bgp')]
#     if bgp_cfg:
#         bgp_cfg = bgp_cfg[0]
#     else:
#         status = 'false'
#         comment += "Конфигурация BGP отсутвует. \n"
#         return {'command': com.command,
#             'check_status': status,
#             'output': output,
#             'comment':  comment
#             }
#     ipv4_family_cfg = [block.strip() for block in out_for_check if block.strip().startswith('ipv4-family unicast')]
#     if ipv4_family_cfg:
#         ipv4_family_cfg = ipv4_family_cfg[0]
#     else:
#         status = 'false'
#         comment += "Конфигурация ipv4-family unicast отсутвует. \n"
#         return {'command': com.command,
#             'check_status': status,
#             'output': 'it\'s output from dis_cur_configuration_bgp func \n\n' + output,
#             'comment':  comment
#             }
#     # check router-id
#     if f"router-id {ip}" not in bgp_cfg:
#         status = 'false'
#         comment += "router-id не совпадает с ip устройства. \n"
    
#     # check use the same as-number
#     as_num_lines = [line for line in bgp_cfg.split("\n") if 'as-number' in line]
#     as_nums = set(int(line.split()[-1].strip()) for line in as_num_lines)
#     if len(as_nums) > 1:
#         status = 'false'
#         comment += f"Используется более одного as-number в конфигурации BGP, это может быть ошибкой \n"
#     as_num = as_nums.pop()
    
#     peer_ip = [ip.strip() for ip in agg_ip.split(",")]
#     result_asg_check = check_bgp_asg(peer_ip, bgp_cfg, ipv4_family_cfg, as_num) 
#     if result_asg_check:
#         status = 'false'
#         comment += result_asg_check
    
#     return {'command': com.command,
#             'check_status': status,
#             'output':  output,
#             'comment':  comment
#             }

# def check_bgp_asg(ip_lilst, bgp, ipv4_uni, as_num):
#     result_bgp = ""
#     result_ipv4 = ""
#     for ip in ip_lilst:
#         if f"peer {ip} as-number {as_num}" not in bgp:
#             result_bgp += f"Конфигурация BGP не содержит строки: peer {ip} as-number {as_num}\n"
#         if f"undo peer {ip} enable" not in ipv4_uni:
#             result_ipv4 += f"Конфигурация ipv4-family unicast не содержит строки: undo peer {ip} enable\n"
#     return result_bgp + result_ipv4

@sync_to_async
def default_command_func(ne, com, *args):
    output = ne.send_command_n3com(com.command)
    check_status = ''
    comment = ''
    if output:
        if com.ok_if_include:
            if search(com.ok_if_include, output):
                check_status = 'ok'
            else: 
                check_status = check_status
        if com.ok_if_exclude:
            if not(search(com.ok_if_exclude, output)):
                check_status = 'ok'  
            else: 
                check_status = 'false'
                comment = com.false_comment
    else:
        check_status = 'ok'
        output = 'Output is empty'
        comment = 'Okay'
    return {'command': com.command,
            'check_status': check_status,
            'output': output,
            'comment': comment
            }


async def run_command_list(ip, username, password, agg_ip, com_list):
    try:
        ne = N3ComSSH(host=ip, username=username, password=password)
        if not(ne is None):
            promt = ne.find_prompt()[:-1]
            yield {'status': f'Подключился к {promt}'}
            await asyncio.sleep(.01)
            for com in com_list:
                func = choose_func(com.command)
                yield await func(ne, com, ip, agg_ip)
                await asyncio.sleep(.01)
    except (NetmikoAuthenticationException, SSHException, NetmikoTimeoutException):
        raise ConnectionError(f'Не удалось подключиться {ip}')
        