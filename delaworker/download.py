import os
import datetime
import random
import time

from randua import generate as get_user_agent
from picklecache import cache
import requests

def headers(user_agent, cookie = None, referer = None):
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
    return requests.get(urls['home'], headers = headers(user_agent), allow_redirects = False)

@cache(os.path.join(os.path.expanduser('~'), '.delaware', week, 'search'))
def _search(firm_file_number, user_agent = None, cookie = None):
    h = headers(user_agent, cookie = cookie, referer = referers['search'])
    return requests.post(urls['search'], headers = h, data = data['search'] % firm_file_number, allow_redirects = False)

@cache(os.path.join(os.path.expanduser('~'), '.delaware', week, 'result'))
def _result(firm_file_number, user_agent = None, cookie = None):
    h = headers(user_agent, cookie = cookie, referer = referers['result'])
    return requests.post(urls['result'], headers = h, data = data['result'] % firm_file_number, allow_redirects = False)

def sleep():
    seconds = sum(random.randint(0,1) for _ in range(100)) / 10
    time.sleep(seconds)
    return seconds

def home():
    'Go to the home page. Cache it for records, but don\'t load from cache.'
    d = datetime.datetime.now()
    return _home(d.strftime('%A/%H:%M:%S'))

def search(home_response, firm_file_number):
    'Search for a firm, loading from the cache if possible'
    user_agent = home_response.request.headers['User-Agent']
    cookie = home_response.headers['Set-Cookie'].split('; ')[0]
    return _search(firm_file_number, user_agent = user_agent, cookie = cookie)

def result(search_response, firm_file_number):
    'Look at detailed information about a firm, loading from the cache if possible'
    user_agent = search_response.request.headers['User-Agent']
    cookie = search_response.request.headers['Cookie']
    return _result(firm_file_number, user_agent = user_agent, cookie = cookie)
