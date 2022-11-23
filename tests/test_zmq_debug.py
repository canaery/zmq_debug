#!/usr/bin/env python

"""Tests for `zmq_debug` package."""

import pytest


from zmq_debug import zmq_debug


@pytest.fixture
def response():
    """Sample workflows fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample workflows test function with the workflows fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
