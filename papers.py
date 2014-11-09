#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """
import re

# imports one per line
import datetime
import json
from pprint import pprint


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """

    # Reading entries
    json_data=open(input_file)
    data = json.load(json_data)
    json_data.close()

    mandatory_fields = ['first_name', 'last_name', 'home', 'birth_date', 'passport', 'from', 'entry_reason']
    loc = ['home', 'from', 'via']
    loc_fl = ['city', 'country', 'region']
    dec_list = []

    # Reading Watchlist Data
    json_data=open(watchlist_file)
    w_data = json.load(json_data)
    json_data.close()

    # Reading Country Data
    json_data=open(countries_file)
    c_data = json.load(json_data)
    json_data.close()

    # List of countries requiring medical advisory
    med_adv_req = []
    for code in c_data:
        if c_data[code]['medical_advisory'] != '':
            med_adv_req.append(code)


    # List of passport numbers that are watch listed
    sec_passport = []
    for i in range(len(w_data)):
        if w_data[i]['passport'] != '':
            sec_passport.append(w_data[i]['passport'].lower())


    # List of names that are watch listed
    sec_name = {}
    for i in range(len(w_data)):
        if w_data[i]['first_name'] != '':
            if w_data[i]['first_name'].lower() in sec_name:
                if w_data[i]['last_name'].lower() not in sec_name[w_data[i]['first_name'].lower()]:
                    sec_name[w_data[i]['first_name'].lower()].append(w_data[i]['last_name'].lower())
            else:
                sec_name[w_data[i]['first_name'].lower()] = [w_data[i]['last_name'].lower()]


    for i in range(len(data)):
        # Check Incomplete INFO
        decision = 0
        for fl in mandatory_fields:
            if fl not in data[i]:
                decision = 'Reject'
        for lc in loc:
            if lc in data[i]:
                for lc_man_fl in loc_fl:
                    if lc_man_fl not in data[i][lc]:
                        decision |= 4

        # Quarantine check - highest priority, we can exit as soon as this condition is met - break
        country_fr = data[i]['from']['country']
        country_via = ''
        if 'via' in data[i]:
            country_via = data[i]['via']['country']

        if country_fr in med_adv_req or country_via in med_adv_req:
            decision |= 8

        # Secondary
        if data[i]['passport'].lower() in sec_passport:
            decision |= 2

        if data[i]['first_name'].lower() in sec_name:
            if data[i]['last_name'].lower() in sec_name[data[i]['first_name'].lower()]:
                decision |= 2

        #  Accept
        if data[i]['entry_reason'] == "returning":
            if data[i]['home']['country'] == "KAN":
                decision |= 1


        if data[i]['entry_reason'].lower() == 'visit' and c_data[data[i]['from']['country']]['visitor_visa_required'] == "1" :
            if 'visa' in data[i] and valid_date_format(data[i]['visa']['date']):
                now = datetime.datetime.now()
                visa_time = data[i]['visa']['date']
                match = re.search(r'([0-9]*)\-', visa_time)
                year = 0
                if match:
                    year = int(match.group(1))

                if now.year - year < 2:
                    decision |= 1
                else:
                    decision |= 4

        if data[i]['entry_reason'].lower() == 'transit' and c_data[data[i]['from']['country']]['transit_visa_required'] == "1" :
            if 'visa' in data[i] and valid_date_format(data[i]['visa']['date']):
                now = datetime.datetime.now()
                visa_time = data[i]['visa']['date']
                match = re.search(r'([0-9]*)\-', visa_time)
                year = 0
                if match:
                    year = int(match.group(1))

                if now.year - year < 2:
                    decision |= 1
                else:
                    decision |= 4

        if decision & 8 == 8:
            dec_list.append('Quarantine')
        else:
            if decision & 4 == 4:
                dec_list.append('Reject')
            else:
                if decision & 2 == 2:
                    dec_list.append('Secondary')
                else:
                    if decision & 1 == 1:
                        dec_list.append('Accept')
                    else:
                        dec_list.append('No decision')

    return dec_list


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



decide('example_entries.json','watchlist.json', 'countries.json')