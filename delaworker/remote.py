from hashlib import sha1

import requests

def salt(username, installation):
    return sha1(manager_address.encode('utf-8') + installation.encode('utf-8')).hexdigest()

def respond(manager_address, username, installation, before_address, file_number, response, finished):
    '''
    finished: whether we are finished with the particular file number
              (whether to mark it on the server as finished)
    '''
    do_something_with(response)
    data = {
        'username': username,
        'salted_installation': salt(username, installation),
        'before_address': before_address,
        'file_number': file_number,
        'finished': finished,
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
