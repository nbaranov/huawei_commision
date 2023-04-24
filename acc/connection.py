from os import getenv
from dotenv import load_dotenv

from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

from getpass_asterisk.getpass_asterisk import getpass_asterisk

# Import or Input Login and Password
def get_username_and_password() -> tuple:
    try:
        load_dotenv() 
        username = getenv("USERNSME")
        password = getenv("PASSWORD")
    except FileNotFoundError:
        username =  input("Input username: ")
        password =  getpass_asterisk("Input password: ")
    return username, password

USERNAME, PASSWORD = get_username_and_password()

# Connection function
def acc_ssh_connect(ip, username=USERNAME, password=PASSWORD) -> ConnectHandler:
    """Returns a BaseConnection if the connection was successful, or None otherwise."""
    dev_info = {
        "device_type": "huawei_ssh",
        "host": ip,
        "timeout": 60,
        "conn_timeout": 60,
        "username": username,
        "password": password,
    }
    try:
        ssh = ConnectHandler(**dev_info)
    except NetmikoAuthenticationException:
        return None
    except NetmikoTimeoutException:
        return None
    else:
        return ssh
        

if __name__ == "__main__":
    # ACC IP with normal RSA key 10.174.68.60
    acc_ne = acc_ssh_connect("10.174.68.60")
    if not(acc_ne is None):
         print("Connected! to ACC with normal RSA key")    
    
    # ACC IP with short RSA key 10.174.100.72
    acc_ne = acc_ssh_connect("10.174.100.72")
    if not(acc_ne is None):
         print("Connected! to ACC with short RSA key")
         