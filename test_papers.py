#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import papers
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


def test_files():
    with papers.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
        decide("", "watchlist.json", "countries.json")
        decide("test_returning_citizen.json", "watchlist.json", "")
        decide("test_watchlist", "watchlist.json", "")
        decide("", "watchlist.json", "countries.json")
        decide("test_watchlist", "", "countries.json")
        decide("test_quarantine", "", "countries.json")
        decide("test_quarantine", "watchlist.json", "")
        decide("", "watchlist.json", "countries.json")

# add functions for other tests
