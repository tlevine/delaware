import random
import time
from hashlib import sha1

import requests

from db import Dadabase

db = Dadabase('sqlite:////home/tlevine/foo.db')

def salt(username, installation):
    return sha1(manager_address.encode('utf-8') + installation.encode('utf-8')).hexdigest()

def respond(manager_address, username, installation, before_address):
    data = {
        'username': username,
        'salted_installation': salt(username, installation),
        'before_address': before_address,
    }
    r = requests.post(manager_address + '/response', data = data)
    return r

def directions(manager_address, username, installation):
    data = {
        'username': username,
        'salted_installation': salt(username, installation),
    }
    r = requests.post(manager_address + '/directions', data = data)
    if r.ok:
        data = json.loads(r.text)
        return data['file_number'], data['before_address']

def sleep():
    seconds = sum(random.randint(0,1) for _ in range(100)) / 10
    time.sleep(seconds)
    return seconds
