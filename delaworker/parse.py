def to_dict(response):
    '''
    Simplify a Response object and dump it to JSON.'
    '''
    request = {
        'body': response.request.body,
        'headers': dict(response.request.headers),
        'method': response.request.method,
        'path_url': response.request.path_url,
        'url': response.request.url,
    }
    return {
       #'apparent_encoding': ,
       #'close': ,
       #'connection': ,
       #'content': ,
        'cookies': dict(response.cookies),
        'elapsed': response.elapsed.microseconds,
        'encoding': response.encoding,
        'headers': dict(response.headers),
       #'history': ,
       #'is_redirect': ,
       #'iter_content': ,
       #'iter_lines': ,
       #'json': ,
       #'links': ,
        'ok': response.ok,
       #'raise_for_status': ,
       #'raw': ,
       #'reason': ,
        'request': request,
        'status_code': response.status_code,
        'text': response.text,
        'url': response.url,
    }

def did_it_work_home(response):
    'I think this always works.'
    return True

def did_it_work_search(response):
    raise NotImplementedError

def did_it_work_result(response):
    raise NotImplementedError
