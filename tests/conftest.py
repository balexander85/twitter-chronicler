"""conftest.py"""

import pytest

from twitter_helpers import fetch_test_data


@pytest.fixture(name="test_status")
def get_test_status():
    def _get_status(key_name):
        return fetch_test_data(key_name)

    return _get_status
