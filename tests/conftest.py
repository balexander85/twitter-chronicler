import pytest

from tests.test_data.generate_test_data import fetch_test_data


@pytest.fixture(name="test_tweet")
def get_test_status():
    def _get_status(key_name):
        return fetch_test_data(key_name)

    return _get_status
