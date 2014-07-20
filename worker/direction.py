import random
import time
from hashlib import sha1

import requests

def auth(manager_address, username, installation):
    password = sha1(manager_address.encode('utf-8') + installation.encode('utf-8')).hexdigest()
    return username, password

def respond(manager_address, username, installation, before_address):
    r = requests.post(manager_address + '/response',
                      auth = auth(manager_address, username, installation),
                      data = {'before_address': before_address})
    return r

def directions(manager_address, username, installation):
    r = requests.post(manager_address + '/directions',
                      auth = auth(manager_address, username, installation))
    if r.ok:
        data = json.loads(r.text)
        return data['file_number'], data['before_address']

def sleep():
    seconds = sum(random.randint(0,1) for _ in range(100)) / 10
    time.sleep(seconds)
    return seconds
