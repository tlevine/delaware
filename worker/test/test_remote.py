import nose.tools as n

import worker.remote as r

def test_salt():
    observed = r.salt('username', 'installation id')
    n.assert_equal(len(observed), 0)
