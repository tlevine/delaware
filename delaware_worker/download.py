import os
import datetime
import random
import time
from logging import getLogger

# from randua import generate as get_user_agent
get_user_agent = lambda: 'https://pypi.python.org/pypi/delaware'
from picklecache import cache
import requests

logger = getLogger('deleworker')

def headers(user_agent, cookie, referer):
    if user_agent == None:
        raise ValueError('User agent may not be None.')
    h = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    if cookie != None:
        h['Cookie'] = cookie
        if referer != None:
            h['Referer'] = referer
        else:
            raise ValueError('A cookie must be provided if a referer has been provided.')
    elif referer != None:
        raise ValueError('A referer must be provided if a cookie has been provided.')
    return h

urls = {
    'home': 'https://delecorp.delaware.gov/tin/GINameSearch.jsp',
    'search': 'https://delecorp.delaware.gov/tin/controller',
    'result': 'https://delecorp.delaware.gov/tin/controller',
}

referers = {
    'home': None,
    'search': urls['home'],
    'result': urls['search'],
}

data = {
    'home': None,
    'search': 'JSPName=GINAMESEARCH&frmEntityName=&frmFileNumber=%d&action=Search',
    'result': 'JSPName=GINAMESEARCH&action=Get+Entity+Details&frmFileNumber=%07d',
}

week = datetime.date.today().strftime('%Y-%W')


@cache(os.path.join(os.path.expanduser('~'), '.delaware', week, 'home'))
def _home(timestamp):
    'Monday/14:50:48, for example'
    user_agent = get_user_agent()
    _headers = headers(user_agent, None, None)
    return requests.get(urls['home'], headers = _headers,
        allow_redirects = False)

@cache(os.path.join(os.path.expanduser('~'), '.delaware', week, 'search'))
def _search(firm_file_number, user_agent = None, cookie = None):
    h = headers(user_agent, cookie, referers['search'])
    return requests.post(urls['search'], headers = h,
        data = data['search'] % firm_file_number, allow_redirects = False)

@cache(os.path.join(os.path.expanduser('~'), '.delaware', week, 'result'))
def _result(firm_file_number, user_agent = None, cookie = None):
    h = headers(user_agent, cookie, referers['result'])
    return requests.post(urls['result'], headers = h,
        data = data['result'] % firm_file_number, allow_redirects = False)

def sleep():
    time.sleep(_sleep_seconds())

def _sleep_seconds():
    return sum(random.randint(0,1) for _ in range(10)) / 5

def home():
    'Go to the home page. Cache it for records, but don\'t load from cache.'
    d = datetime.datetime.now()
    response = _home(d.strftime('%A/%H:%M:%S'))
    logger.info('Downloaded %s' % response.url)
    return response

def search(home_response, firm_file_number):
    'Search for a firm, loading from the cache if possible'
    user_agent = home_response.request.headers['User-Agent']
    cookie = home_response.headers['Set-Cookie'].split('; ')[0]
    response = _search(firm_file_number, user_agent = user_agent, cookie = cookie)
    logger.info('Downloaded %s for file number %07d' % (response.url, firm_file_number))
    return response

def result(search_response, firm_file_number):
    'Look at detailed information about a firm, loading from the cache if possible'
    user_agent = search_response.request.headers['User-Agent']
    cookie = search_response.request.headers['Cookie']
    response = _result(firm_file_number, user_agent = user_agent, cookie = cookie)
    logger.info('Downloaded %s for file number %07d' % (response.url, firm_file_number))
    return response
