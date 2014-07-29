import os
from functools import partial

import worker.local as local
import worker.download as dl
import worker.remote as remote
import worker.parse as parse
from worker.params import params

ca_bundle_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'certificates', 'delaware.dada.pink.crt')

def work(local = False):
    if local:
        respond = local.respond
        directions = local.directions
    else:
        manager_address, username, installation = params()
        respond = partial(remote.respond, ca_bundle_file, parse.to_dict, manager_address, username, installation)
        directions = partial(remote.directions, ca_bundle_file, manager_address, username, installation)
    sleep = dl.sleep
    home_response = None
    while True:
        firm_file_number, before_address = get_work(directions, sleep)
        home_response = do_work(home_response, firm_file_number, partial(respond, before_address, firm_file_number))

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

    search_response = dl.search(home_response, firm_file_number)
    respond(search_response, parse.did_it_work_search(search_response))
    if not parse.is_session_valid(search_response):
        return None

    result_response = dl.result(search_response, firm_file_number)
    respond(result_response, parse.did_it_work_result(result_response))
    if not parse.is_session_valid(result_response):
        return None

    return home_response
