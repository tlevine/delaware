import nose.tools as n

import worker.remote as r

def test_salt():
    observed = r.salt('manager address', 'installation id')
    n.assert_equal(len(observed), 40)
