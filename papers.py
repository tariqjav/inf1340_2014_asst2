#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import datetime


# All the information that an Immigration Officer will input to inspect entry for an individual:

first_name = input("First Name:")

last_name = input("Last Name:")

birth_date = input("Date in YYYY-MM-DD:")

passport_number = input("Passport Number:")

home_location_city = input("Home City:")
home_location_region = input("Home Region:")
home_location_country = input("Home Country Code:")

from_location_city = input("From City:")
from_location_region = input("From Region:")
from_location_country = input("From Country Code:")

reason_for_entry = input("Returning, Transit or Visa?:")

if reason_for_entry == "Transit":
    via_location_city = input("Via City:")
    via_location_region = input("Via Region:")
    via_location_country = input("Via Country Code:")
    visa_date = input("Date in YYYY-MM-DD:")
    visa_code = input("Visa Code")

elif reason_for_entry == "Visa":
    visa_date = input("Date in YYYY-MM-DD:")
    visa_code = input("Visa Code")





def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    return ["Reject"]


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False



