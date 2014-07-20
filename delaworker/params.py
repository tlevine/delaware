import configparser
import uuid

SECTION = 'worker'
CONFIG = os.path.expanduser(os.path.join('~', '.deleware', 'config')

def params():
    from_config = read_config_params()
    if from_config == None:
        manager_address, username = prompt_params()
        installation = installation_id()
        write_config_params(manager_address, username, installation, open(CONFIG, 'w'))
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
    username = input('Username: ')
    return manager_address, username

def read_config_params():
    c = configparser.ConfigParser()
    c.read(CONFIG)

    manager_address = c.get(SECTION, 'manager_address', fallback = None)
    username = c.get(SECTION, 'username', fallback = None)
    installation = c.get(SECTION, 'installation', fallback = None)

    if manager_address != None and username != None and installation != None):
        return manager_address, username, installation

def write_config_params(manager_address, username, installation, fp):
    c = configparser.ConfigParser()
    c.set(SECTION, 'manager_address', value = manager_address)
    c.set(SECTION, 'username', value = username)
    c.set(SECTION, 'installation', installation = installation)
    c.write(fp)
