from functools import partial

import delaworker.local as local
import delaworker.download as dl
import delaworker.remote as remote
import delaworker.parse as parse
from delaworker.params import params, argparser

def work(local = False):
    if local:
        respond = local.respond
        directions = local.directions
    else:
        manager_address, username, installation = params()
        respond = partial(remote.respond, parse.to_json, manager_address, username, installation)
        directions = partial(remote.directions, manager_address, username, installation)
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
    'Given a firm file number, try to get the information.'
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
