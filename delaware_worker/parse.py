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

def did_it_work_search(firm_file_number, response):
    '''
    If it worked, the file number shows up in both
    the search bar and the result list. If it didn't,
    the file number shows up only in the search bar.
    '''
    return response.text.count('%07d' % firm_file_number) == 3

def did_it_work_result(firm_file_number, response):
    '''
    If it worked, the file number shows up in both
    a hidden input field and the "File Number" field.
    If it didn't, the file number shows up only in
    the search bar.
    '''
    return response.text.count('%07d' % firm_file_number) == 2


def is_session_valid(response):
    '''
    It's not valid if you see something like this.

    > ERROR SCREEN
    >
    > System error has occurred with the following error message
    >
    > Illegal Attempt
    >
    > Please logout and report this problem to help desk.
    >
    > Thank you.

    '''
    return 'Illegal Attempt' not in response.text
