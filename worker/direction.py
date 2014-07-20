import random
import time
from hashlib import sha1

import requests

def auth(manager_address, username, installation):
    password = sha1(manager_address.encode('utf-8') + installation.encode('utf-8')).hexdigest()
    return username, password

def respond(manager_address, username, installation, before_address):
    return requests.post(manager_address + '/respond',
                         auth = auth(manager_address, username, installation),
                         data = {'before_address': before_address})

def directions(manager_address, username, installation):
    return requests.post(manager_address + '/direct

def sleep():
    seconds = sum(random.randint(0,1) for _ in range(100)) / 10
    time.sleep(seconds)
    return seconds
