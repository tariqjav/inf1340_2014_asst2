#!/usr/bin/env python3

""" Module to test papers.py  """

# imports one per line
import pytest
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]

def test_files():
    with pytest.raises(IOError):
        decide("test_returning_citizen.json", "", "countries.json")
    with pytest.raises(IOError):
        decide("", "watchlist.json", "countries.json")
    with pytest.raises(IOError):
        decide("test_returning_citizen.json", "watchlist.json", "")
    with pytest.raises(IOError):
        decide("test_watchlist", "watchlist.json", "")
    with pytest.raises(IOError):
        decide("", "watchlist.json", "countries.json")
    with pytest.raises(IOError):
        decide("test_watchlist.json", "", "countries.json")
    with pytest.raises(IOError):
        decide("test_quarantine.json", "", "countries.json")
    with pytest.raises(IOError):
        decide("test_quarantine", "watchlist.json", "")
    with pytest.raises(IOError):
        decide("", "watchlist.json", "countries.json")

    # When file not passed are not string
    with pytest.raises(TypeError):
        decide(1, "watchlist.json", "countries.json")

    with pytest.raises(TypeError):
        decide("test_returning_citizen.json", 1, "countries.json")

    # When file not passed are not json
    with pytest.raises(TypeError):
        decide("a", "watchlist.json", "countries.json")

    with pytest.raises(TypeError):
        decide("test_returning_citizen.json", "a", "countries.json")

    # Wrong data structure in json passed
    with pytest.raises(ValueError):
        decide("countries.json", "watchlist.json", "countries.json")

    with pytest.raises(ValueError):
        decide("test_returning_citizen.json", "countries.json", "countries.json")

    with pytest.raises(ValueError):
        decide("test_returning_citizen.json", "watchlist.json", "watchlist.json")


# add functions for other tests
test_basic()
test_files()