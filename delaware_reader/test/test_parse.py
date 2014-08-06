import os, json

import nose.tools as n

import delaware_reader.parse as p

with open(os.path.join('delaware_reader', 'test', 'fixtures', 'result-response.json')) as fp:
    result = json.load(fp)
with open(os.path.join('delaware_reader', 'test', 'fixtures', 'direction-response.json')) as fp:
    direction = json.load(fp)

def test_parse():
    observed = dict(p.parse(result))
    expected = {
        'datetime_received': '2014-07-29T22:03:28.875019',
        'address': '1013 CENTRE RD STE 403-A',
        'city': 'WILMINGTON',
        'country': 'NEW CASTLE',
        'entity_date': '09/10/2009',
        'entity_kind': 'LIMITED LIABILITY COMPANY (LLC)',
        'entity_name': 'IDR MARKETING LLC',
        'entity_type': 'GENERAL',
        'file_number': '4729208',
        'name': 'REGISTERED AGENTS, LTD.',
        'phone': '(302)421-5750',
        'postcode': '19805',
        'residency': 'DOMESTIC',
        'state': 'DE',
    }
    n.assert_dict_equal(observed, expected)

def test_is_entity_detail():
    n.assert_false(p.is_entity_detail(direction))
    n.assert_true(p.is_entity_detail(result))
