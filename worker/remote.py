from hashlib import sha1

import requests

def salt(manager_address, installation):
    return sha1(manager_address.encode('utf-8') + installation.encode('utf-8')).hexdigest()

def respond(verify, to_dict, manager_address, username, installation, before_address, file_number, response, finished):
    '''
    finished: whether we are finished with the particular file number
              (whether to mark it on the server as finished)
    '''
    if verify == None:
        verify = True
    data = {
        'username': username,
        'salted_installation': salt(username, installation),
        'before_address': before_address,
        'file_number': file_number,
        'finished': finished,
        'response': to_dict(response)
    }
    r = requests.post(manager_address + '/response', data = data, verify = verify)
    return r.json()['ip_address']

def directions(verify, manager_address, username, installation):
    if verify == None:
        verify = True
    data = {
        'username': username,
        'salted_installation': salt(username, installation),
    }
    r = requests.post(manager_address + '/directions', data = data, verify = verify)
    if r.ok:
        data = r.json()
        return data['file_number'], data['ip_address']
