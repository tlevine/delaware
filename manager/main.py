from bottle import Bottle, run, request, response

from manager.db import Dadabase
from manager.args import parser

args = parser.parse_args()
db = Dadabase(args.database, args.request_directory)
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

app = b
