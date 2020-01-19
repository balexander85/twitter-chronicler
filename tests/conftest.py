import pytest

from .test_data.twitter_data import quoted_tweet, basic_tweet, mock_status


@pytest.fixture(scope="session", name="quoted_tweet")
def get_test_quoted_status():
    return quoted_tweet


@pytest.fixture(scope="session", name="basic_tweet")
def get_test_basic_status():
    return basic_tweet


@pytest.fixture(scope="session", name="mock_status")
def get_mock_status():
    return mock_status
