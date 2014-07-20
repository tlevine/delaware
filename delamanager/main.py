from bottle import Bottle, run, request, response

from db import Dadabase

db = Dadabase('sqlite:////home/tlevine/foo.db')
b = Bottle()

@b.post('/directions')
def directions():
    before = request.remote_route
    if db.under_limit(before):
        response.status_code = 200
        return json.dumps({
            'before_address': before,
            'file_number': db.file_number(),
        })
    else:
        response.status_code = 429

@b.post('/response')
def response():
    after = request.remote_route
    db.
