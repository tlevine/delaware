DB = None


def at_limit(ip_address):
    params = []
    blah = DB.execute('SELECT count(*) FROM requests WHERE datetime > ? AND ip_address > ?', params)
