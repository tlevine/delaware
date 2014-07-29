import datetime

import bottle

import shared.log
from manager.db import Dadabase
from manager.args import parser

args = parser.parse_args()
db = Dadabase(args.database, args.request_directory)
b = bottle.Bottle()
logger = shared.log.output('delemanager', filename = args.logfile)

@b.hook('before_request')
def log():
    logger.info('{ip} - - [{time}] "{method} {uri} {protocol}" {status}'.format(
        ip = bottle.request.environ.get('REMOTE_ADDR'),
        time = datetime.datetime.now().isoformat(),
        method = bottle.request.environ.get('REQUEST_METHOD'),
        uri = bottle.request.environ.get('REQUEST_URI'),
        protocol = bottle.request.environ.get('SERVER_PROTOCOL'),
        status = bottle.response.status_code,
    ))
    db.save_request(bottle.request)


def rate_limit(f):
    def wrapper():
        if db.under_limit(bottle.request.remote_route):
            return f()
        else:
            bottle.response.status_code = 429
    return wrapper

@b.post('/directions')
@rate_limit
def directions():
    ip_address = bottle.request.remote_route
    return {
        'ip_address': ip_address,
        'file_number': db.file_number(),
    }

@b.post('/response')
@rate_limit
def response():
    ip_address = bottle.request.remote_route
    return {
        'ip_address': ip_address,
    }

@b.get('<_:path>'):
def info(_):
    bottle.redirect('http://small.dada.pink/delaware/README')

app = b
