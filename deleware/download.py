# from randua import generate as user_agent


def headers(user_agent, cookie = None, referer = None):
    h = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
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
