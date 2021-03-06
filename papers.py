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

    # Check for input data type: TYPE ERROR if wrong values passed
    if not type(input_file) is str:
        raise TypeError("Type Error: Pass in file name")

    if not type(watchlist_file) is str:
        raise TypeError("Type Error: Pass in file name")

    if not type(countries_file) is str:
        raise TypeError("Type Error: Pass in file name")

    if input_file == "" or watchlist_file == "" or countries_file == "":
        raise FileNotFoundError("FileNotFoundError: No File name passed")

    # Check if data files are of json types: TYPE ERROR if wrong values passed
    match = re.search(r'([^.]*.json)', input_file)
    if not match:
        raise TypeError("Type Error: Pass in a json file name")

    match = re.search(r'([^.]*.json)', watchlist_file)
    if not match:
        raise TypeError("Type Error: Pass in a json file name")

    match = re.search(r'([^.]*.json)', countries_file)
    if not match:
        raise TypeError("Type Error: Pass in a json file name")


    ####################################################################
    # Python will raise IO ERROR if file not found in json --> Expected
    # To throw normal FileNotFoundError: I will read all the files first
    ####################################################################

    # This will read the input entries of an individual
    try:
        input_file_f = open(input_file, 'r')
        json_data=open(input_file)
        data = json.load(json_data)
        json_data.close()
    except FileNotFoundError:
        raise FileNotFoundError
    except IOError:
        raise FileNotFoundError

    # This will check the data structure in the json for input_file
    #    ------     Has to be a list of dictionaries
    if type(data) is list:
        for i in range(len(data)):
            if not type(data[i]) is dict:
                raise ValueError("Value Error: input_file type is wrong")
    else:
        raise ValueError("Value Error: input_file type is wrong")


    # Mandatory fields, location fields {mandatory location fields}
    mandatory_fields = ['first_name', 'last_name', 'home', 'birth_date', 'passport', 'from', 'entry_reason']
    loc = ['home', 'from', 'via']
    loc_fl = ['city', 'country', 'region']

    # List of string which holds the final decision for every single case.
    dec_list = []


    # This will read the Watchlist Data
    try:
        watchlist_file_f = open(watchlist_file, 'r')
        json_data=open(watchlist_file)
        w_data = json.load(json_data)
        json_data.close()
    except FileNotFoundError:
        raise FileNotFoundError
    except IOError:
        raise FileNotFoundError

    # This will check the data structure in the json for watchlist_file
    #    ------      Has to be a list of dictionaries
    if type(w_data) is list:
        for i in range(len(w_data)):
            if not type(w_data[i]) is dict:
                raise ValueError("Value Error: watchlist_file type is wrong")
    else:
        raise ValueError("Value Error: watchlist_file type is wrong")

    # This will read Country Data
    try:
        countries_file_f = open(countries_file, 'r')
        json_data=open(countries_file)
        c_data = json.load(json_data)
        json_data.close()
    except FileNotFoundError:
        raise FileNotFoundError
    except IOError:
        raise FileNotFoundError



    # This will check the data structure in the json for countries_file
    #    ------      Has to be dictionary of dictionaries
    if type(c_data) is dict:
        for key in c_data:
            if not type(c_data[key]) is dict:
                raise ValueError("Value Error: countries_file file type is wrong")
    else:
        raise ValueError("Value Error: countries_file file type is wrong")



    # This will create a List of countries requiring medical advisory
    # It is more efficient to be outside loop

    med_adv_req = []
    for code in c_data:
        if c_data[code]['medical_advisory'] != '':
            med_adv_req.append(code)


    # This will create a list of passport numbers that are watch listed
    sec_passport = []
    for i in range(len(w_data)):
        if w_data[i]['passport'] != '':
            sec_passport.append(w_data[i]['passport'].lower())


    # This will create a dictionary of full names of individuals that are watch listed
    # --> it will be easier and faster to search later on in the main for loop that loops over entries
    sec_name = {}
    for i in range(len(w_data)):
        if w_data[i]['first_name'] != '':
            if w_data[i]['first_name'].lower() in sec_name:
                if w_data[i]['last_name'].lower() not in sec_name[w_data[i]['first_name'].lower()]:
                    sec_name[w_data[i]['first_name'].lower()].append(w_data[i]['last_name'].lower())
            else:
                sec_name[w_data[i]['first_name'].lower()] = [w_data[i]['last_name'].lower()]



    # Main for loop that loops over all entries on input file and makes decision
    for i in range(len(data)):

        # This will check incomplete information
        decision = 0
        for fl in mandatory_fields:
            if fl not in data[i]:
                decision |= 4

        for lc in loc:
            if lc in data[i]:
                for lc_man_fl in loc_fl:
                    if lc_man_fl not in data[i][lc]:
                        decision |= 4


        # This will perform a check for individuals who should be in Quarantine- highest priority
        if 'from' in data[i]:
            country_fr = data[i]['from']['country']
            country_via = ''
            if 'via' in data[i]:
                country_via = data[i]['via']['country']

            if country_fr in med_adv_req or country_via in med_adv_req:
                decision |= 8

        # To make sure explicitly calling mandatory fields only if they exist
        if decision & 4 != 4:
            # This will perform a check to see who would be granted the Secondary decision
            if data[i]['passport'].lower() in sec_passport:
                decision |= 2

            # if passport not have valid format -- Not in assignment handout
            if not valid_passport_format(data[i]['passport'].lower()):
                decision |= 4

            if data[i]['first_name'].lower() in sec_name:
                if data[i]['last_name'].lower() in sec_name[data[i]['first_name'].lower()]:
                    decision |= 2

            #  This will perform a check to see who would be granted the Accept decision
            if data[i]['entry_reason'] == "returning":
                if data[i]['home']['country'] == "KAN":
                    decision |= 1


            # This section is to handle the cases, when user is visiting from a country that visiting
            if data[i]['entry_reason'].lower() == 'visit' and c_data[data[i]['from']['country']]['visitor_visa_required'] == "1" :
                if 'visa' in data[i] and valid_date_format(data[i]['visa']['date']):
                    now = datetime.datetime.now()
                    visa_time = data[i]['visa']['date']
                    match = re.search(r'([0-9]*)\-', visa_time)
                    year = 0
                    if match:
                        year = int(match.group(1))

                    if now.year - year < 2:
                        # Accept if visa is within 2 yrs
                        decision |= 1
                    else:
                        # Reject otherwise
                        decision |= 4
                else:
                    # if it is not a valid date or no visa
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
                        # Accept if visa is within 2 yrs
                        decision |= 1
                    else:
                        # Reject otherwise
                        decision |= 4
                else:
                    # if it is not a valid date or no visa --> Not in handout
                    decision |= 4


        # This will take into account the priorities, it will check quarantine first
        # then, we will have reject and at the end, we have secondaries and accept.
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
                        dec_list.append('Accept') # I think this should be accept?


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

