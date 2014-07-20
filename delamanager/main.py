
from bottle import Bottle, run, request, response
b = Bottle()

@b.post('/v1/')
def directions():
    return json.dumps({
        'before_address': request.remote_route,
    })

def response():
    return json.dumps({
    })
