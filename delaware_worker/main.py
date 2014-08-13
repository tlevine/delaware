import os
from functools import partial
import time

import requests.exceptions

import delaware_shared.log
import delaware_worker.local as local
import delaware_worker.download as dl
import delaware_worker.remote as remote
import delaware_worker.parse as parse
from delaware_worker.params import params

def work(local = False):
    if local:
        respond = local.respond
        directions = local.directions
    else:
        ca_bundle_file, manager_address, username, installation = params()
        respond = partial(remote.respond, ca_bundle_file, parse.to_dict, manager_address, username, installation)
        directions = partial(remote.directions, ca_bundle_file, manager_address, username, installation)
    sleep = dl.sleep
    home_response = None

    logger = delaware_shared.log.output('deleworker',
        filename = os.path.join(os.path.expanduser('~'), '.delaware', 'worker.log'))
    while True:
        try:
            firm_file_number, before_address = get_work(directions, sleep)
            home_response = do_work(home_response, firm_file_number, partial(respond, before_address, firm_file_number))
        except requests.exceptions.ConnectionError:
            logger.info('Waiting a minute because the internet connection is bad')
            time.sleep(60) # Wait a minute, and try again.

def get_work(directions, sleep):
    '''
    Periodically poll for work orders.
    Return the work orders if there are any
    or None if there aren't.
    '''
    while True:
        answer = directions()
        if answer == None:
            sleep()
        else:
            return answer

def do_work(home_response, firm_file_number, respond, dl = dl):
    '''
    Given a firm file number, try to get the information.

    If the session is still valid, return the home_response
    so the cookie can be reused.
    '''
    if home_response == None:
        home_response = dl.home()
        respond(home_response, False)
        dl.sleep()

    search_response = dl.search(home_response, firm_file_number)
    respond(search_response, parse.did_it_work_search(firm_file_number, search_response))
    dl.sleep()
    if not parse.is_session_valid(search_response):
        return None

    result_response = dl.result(search_response, firm_file_number)
    respond(result_response, parse.did_it_work_result(firm_file_number, result_response))
    dl.sleep()
    if not parse.is_session_valid(result_response):
        return None

    return home_response
