from functools import partial

import delaworker.local as local
import delaworker.download as dl
import delaworker.direction as d
from delaworker.params import params

def work(local = False):
    if local:
        respond = local.respond
        directions = local.directions
    else:
        manager_address, username, installation = params()
        respond = partial(d.respond, manager_address, username, installation)
        directions = partial(d.directions, manager_address, username, installation)
    sleep = d.sleep
    while True:
        firm_file_number, before_address = get_work(directions, sleep)
        do_work(firm_file_number, partial(respond, before_address, firm_file_number))

def get_work(directions, sleep):
    while True:
        answer = directions()
        if answer == None:
            sleep()
        else:
            return answer

def do_work(firm_file_number, respond, dl = dl):
    'Given a firm file number, try to get the information.'
    home_response = dl.home()
    respond(home_response, False)
    for firm_file_number in firm_file_numbers:
        search_response = dl.search(home_response, firm_file_number)
        respond(search_response, False)
        result_response = dl.result(search_response, firm_file_number):
        respond(result_response, True)
