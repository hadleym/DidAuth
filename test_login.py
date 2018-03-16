from login import authenticate, resolve
import json

def test_login():
    did = '2hoqvcwupRTUNkXn6ArYzs'
    assert authenticate(did) is True
    assert resolve(did) is None
    did2 = 'did:sov:WRfXPg8dantKVubE3HX8pw'
    result_json = json.loads(resolve(did))
    assert result_json['control'] is not None