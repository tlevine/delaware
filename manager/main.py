from bottle import Bottle, run, request, response

from db import Dadabase

db = Dadabase('sqlite:////home/tlevine/foo.db', '/home/tlevine/foo')
b = Bottle()

def rate_limit(f):
    def wrapper():
        if db.under_limit(request.remote_route):
            return f()
        else:
            response.status_code = 429
    return wrapper

@b.post('/directions')
@rate_limit
def directions():
    db.save_request(request)
    ip_address = request.remote_route
    return {
        'ip_address': ip_address,
        'file_number': db.file_number(),
    }

@b.post('/response')
@rate_limit
def response():
    db.save_request(request)
    ip_address = request.remote_route
    return {
        'ip_address': ip_address,
    }
