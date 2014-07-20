from bottle import Bottle, run, request, response

import db

b = Bottle()

@b.post('/v1/')
def directions():
    before = request.remote_route
    if db.at_limit(before):
        response.status_code = 429
    else:
        return json.dumps({
            'before_address': before,
            'file_number': db.file_number(),
        })

def response():
    return json.dumps({
    })
