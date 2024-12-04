from keys import generate_key_pair, get_active_keys
import datetime

def test_key_generation():
    keys = generate_key_pair()
    assert len(keys) > 0
    assert "kid" in keys[0]

def test_active_keys():
    keys = generate_key_pair()
    active_keys = get_active_keys(keys)
    assert len(active_keys) > 0
    assert "kid" in active_keys[0]
