import os
import pickle
from functools import partial

import nose.tools as n

import worker.parse as p

FIXTURES = os.path.join('worker', 'test', 'fixtures')

def test():
    for testcase in TESTCASES:
        yield testcase

def check(function, firm_file_number, filename, expectatation)
    with open(os.path.join(FIXTURES, filename), 'rb') as fp:
        error, response = pickle.load(fp)
    n.assert_equal(function(firm_file_number, response), expectation)

def check_is_session_valid(filename, expectatation)
    with open(os.path.join(FIXTURES, filename), 'rb') as fp:
        error, response = pickle.load(fp)
    n.assert_equal(p.is_session_valid(response), expectation)

check_did_it_work_search = partial(check, p.did_it_work_search)
check_did_it_work_result = partial(check, p.did_it_work_result)

def check_to_json(filename):
    with open(os.path.join(FIXTURES, filename), 'rb') as fp:
        error, response = pickle.load(fp)
    with open(os.path.join(FIXTURES, filename + '.json'), 'r') as fp:
        expectation = json.load(fp)
    n.assert_dict_equal(p.to_json(response), expectation)

TESTCASES = [
    (check_is_session_valid, 'home-working', True),
    (check_is_session_valid, 'result-ed100', True),
    (check_is_session_valid, 'result-success', True),
    (check_is_session_valid, 'search-match-found-dada', True),
    (check_is_session_valid, 'search-match-found-toilet', True),
    (check_did_it_work_result, 0, 'result-ed100', True),
    (check_did_it_work_result, 0, 'result-success', True),
    (check_did_it_work_search, 0, 'search-match-found-dada', True),
    (check_did_it_work_search, 0, 'search-match-found-toilet', True),
    (check_to_json, 'home-working'),
    (check_to_json, 'result-ed100'),
    (check_to_json, 'result-success'),
    (check_to_json, 'search-match-found-dada'),
    (check_to_json, 'search-match-found-toilet'),
]
