import sys
from connection import acc_ssh_connect, get_username_and_password
from os.path import dirname, abspath, join
from os import getenv
from dotenv import load_dotenv


# import modules
import alarms_ms
import software
import state


load_dotenv()
IP = getenv("IP")

# connect
acc_ne = acc_ssh_connect(IP, *get_username_and_password())

# Alarms and Management System
alarms_ms.check(acc_ne, IP)

# Software check functions 
software.check(acc_ne, IP)

# State check
state.check(acc_ne, IP)
