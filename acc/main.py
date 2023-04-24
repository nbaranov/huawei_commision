import sys
from connection import acc_ssh_connect, get_username_and_password
from os.path import dirname, abspath, join
from os import getenv
from dotenv import load_dotenv


THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)
from output import log_commission

# import modules
import software


load_dotenv()
IP = getenv("IP")

# connect
acc_ne = acc_ssh_connect(IP, *get_username_and_password())

# Software check functions 
output = software.display_version(acc_ne)
log_commission(IP, *output)
output = software.display_startup(acc_ne)
log_commission(IP, *output)
output = software.display_patch_information(acc_ne)
log_commission(IP, *output)
