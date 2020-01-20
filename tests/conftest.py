import pytest

from tests.test_data.generate_test_data import test_tweet


@pytest.fixture(name="test_tweet")
def get_test_status():
    def _get_status(key_name):
        return test_tweet.get(key_name)

    return _get_status
