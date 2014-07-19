from randua import generate as get_user_agent
from picklecache import cache

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
    'result': 'JSPName=GINAMESEARCH&action=Get+Entity+Details&frmFileNumber=%d',
}

@cache(os.path.join(os.path.expanduser('~'), '.deleware', 'home'))
def home(page, date, user_agent = None):
    return requests.get(urls['home'], headers = headers(user_agent))

@cache(os.path.join(os.path.expanduser('~'), '.deleware', 'search'))
def search(page, firm_file_number, user_agent = None, cookie = None):
    h = headers(user_agent, cookie = cookie, referer = referers['search'])
    return requests.post(urls['search'], headers = h, data = data['search'] % firm_file_number)

@cache(os.path.join(os.path.expanduser('~'), '.deleware', 'result'))
def result(page, firm_file_number, user_agent = None, cookie = None):
    h = headers(user_agent, cookie = cookie, referer = referers['result'])
    return requests.post(urls['result'], headers = h, data = data['result'] % firm_file_number)
