import configparser
import os
import uuid
from getpass import getuser

SECTION = 'worker'
DIRECTORY = os.path.expanduser(os.path.join('~', '.delaware'))
CONFIG = os.path.join(DIRECTORY, 'config')

def params():
    from_config = read_config_params(CONFIG)
    if from_config == None:
        manager_address, username = prompt_params()
        installation = installation_id()
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
        write_config_params(manager_address, username, installation, CONFIG)
    else:
        manager_address, username, installation = from_config

    return manager_address, username, installation

def installation_id():
    return str(uuid.uuid4())

def prompt_params():
    default_manager_address = 'https://delaware.dada.pink'
    manager_address = input('Manager [%s]: ' % default_manager_address)
    if manager_address == '':
        manager_address = default_manager_address

    default_username = getuser()
    username = input('Username [%s]: ' % default_username)
    if username == '':
        username = default_username

    return manager_address, username

def read_config_params(filename):
    c = configparser.ConfigParser()
    c.read(filename)

    manager_address = c.get(SECTION, 'manager_address', fallback = None)
    username = c.get(SECTION, 'username', fallback = None)
    installation = c.get(SECTION, 'installation', fallback = None)

    if manager_address != None and username != None and installation != None:
        return manager_address, username, installation

def write_config_params(manager_address, username, installation, filename):
    c = configparser.ConfigParser()
    c.add_section(SECTION)
    c.set(SECTION, 'manager_address', value = manager_address)
    c.set(SECTION, 'username', value = username)
    c.set(SECTION, 'installation', value = installation)
    with open(filename, 'w') as fp:
        c.write(fp)
