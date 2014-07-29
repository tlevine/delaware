import json
from hashlib import sha1
from logging import getLogger

import requests

logger = getLogger('deleworker')

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
    r = post(verify, manager_address + '/response', data = data)
    logger.info('Uploaded a %07d response' % file_number)
    return r.json()['ip_address']

def directions(verify, manager_address, username, installation):
    if verify == None:
        verify = True
    data = {
        'username': username,
        'salted_installation': salt(username, installation),
    }
    r = post(verify, manager_address + '/directions', data)
    if r.ok:
        data = r.json()
        logger.info('Received directions to query %07d' % data['file_number'])
        return data['file_number'], data['ip_address']

HEADERS = {
    'content-type': 'application/json',
}
def post(verify, url, data):
    return requests.post(url, data = json.dumps(data), verify = verify, headers = HEADERS)
