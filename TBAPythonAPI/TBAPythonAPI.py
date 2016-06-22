import os
import sys
import requests
import numpy as np
from numpy import array as np_array

class TBAParser:
    def __init__(self, teamNumber, packageID, versionID):
        self.teamNumber = teamNumber
        self.packageID = packageID
        self.versionID = versionID
        self.header = {'X-TBA-App-Id': 'frc{team}:{package}:{version}'.format(team = teamNumber, package = packageID, version = versionID)}
        self.baseURL = 'http://www.thebluealliance.com/api/v2'

    #Team Info

    def get_team_obj(self, team_number):
        request = (self.baseURL + "/team/frc" + str(team_number))
        response = requests.get(request, headers = self.header)
        dictionary = response.json()
        return dictionary

    def get_team_full_name(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        full_name = team_dictionary['name']
        return full_name

    def get_team_nick_name(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        nick_name = team_dictionary['nickname']
        return nick_name

    def get_team_number(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        team_number = team_dictionary['team_number']
        return team_number

    def get_team_rookie_year(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        rookie_year = team_dictionary['rookie_year']
        return rookie_year

    def get_team_website(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        website = team_dictionary['website']
        return website

    def get_team_city(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        city = team_dictionary['locality']
        return city

    def get_team_region(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        region = team_dictionary['region']
        return region

    def get_team_location(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        location = team_dictionary['location']
        return location

    def get_team_key(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        key = team_dictionary['key']
        return key

    def get_team_country(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        country = team_dictionary['country_name']
        return country

    def get_team_motto(self, team_number):
        team_dictionary = self.get_team_obj(team_number)
        motto = team_dictionary['motto']
        return motto


    #Event Info

    #Finds event key from both year and event nickname.
    #Name variable does not have to be complete, but it must be properly capitalized and specific enough to specify a single event
    #Returns "0" is no events are found, "1" if more than one event is found, and event key otherwise.
    #ALL RETURNS ARE STRINGS
    #Based on method from https://github.com/Alexanders101/The-Blue-Alliance-Python-API/
    def find_event_key(self, year, name):
        request = (self.baseURL + "/events/" + str(year))
        response = requests.get(request, headers = self.header)
        dictionary = response.json()
        events = np_array([[str(event['short_name']), str(event['key'])] for event in dictionary])
        if name is 'all':
            return events
        else:
            ret = ''
            for sub in events[:, 0]:
                if sub[:len(name)] == name:
                    if not ret == '':
                        print("Multiple events found. Please refine your search.")
                        return '1'
                    ret = sub
            curr = events[events[:, 0] == ret]
            if len(ret) == 0:
                print('No events found. Please ensure spelling and capitalization are correct.')
                return '0'
            return curr[0][1]

    def get_event_obj(self, eventKey): #Returns json array of event from event key
        request = (self.baseURL + "/event/" + eventKey)
        response = requests.get(request, headers = self.header)
        dictionary = response.json()
        return dictionary

    def get_event_key(self, eventKey): #Returns event key of event from event key - Useless but redundant
        event_dictionary = self.get_event_obj(eventKey)
        event_key = event_dictionary['key']
        return event_key

    def get_event_website(self, eventKey): #Returns event website from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_website = event_dictionary['website']
        return event_website

    def get_event_is_official(self, eventKey): #Returns boolean whether event is official from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_is_official = event_dictionary['official']
        return event_is_official

    def get_event_end_date(self, eventKey): #Returns end date of event from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_end_date = event_dictionary['end_date']
        return event_end_date

    def get_event_name(self, eventKey): #Returns event name from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_name = event_dictionary['name']
        return event_name

    def get_event_short_name(self, eventKey): #Returns event short name from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_short_name = event_dictionary['short_name']
        return event_short_name

    def get_event_facebook_eid(self, eventKey): #Returns event facebook eid from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_facebook_eid = event_dictionary['facebook_eid']
        return event_facebook_eid

    def get_event_district_string(self, eventKey): #Returns event district string from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_district_string = event_dictionary['event_district_string']
        return event_district_string

    def get_event_venue_address(self, eventKey): #Returns event venue address from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_venue_address = event_dictionary['venue_address']
        return event_venue_address

    def get_event_district(self, eventKey): #Returns event district key from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_district = event_dictionary['event_district']
        return event_district

    def get_event_location(self, eventKey): #Returns event location from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_location = event_dictionary['location']
        return event_location

    def get_event_code(self, eventKey): #Returns event code from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_code = event_dictionary['event_code']
        return event_code

    def get_event_year(self, eventKey): #Returns event year from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_year = event_dictionary['year']
        return event_year

    def get_event_webcast(self, eventKey): #Returns event webcast url from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_webcast = event_dictionary['webcast']
        return event_webcast

    def get_event_timezone(self, eventKey): #Returns event timezone from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_timezone = event_dictionary['timezone']
        return event_timezone

    def get_event_alliances(self, eventKey): #Returns json array of alliances in event from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_alliances = event_dictionary['alliances']
        return event_alliances

    def get_event_alliance(self, eventKey, number): #Returns json array of alliance (declines and members) in event from event key and alliance seed
        event_dictionary = self.get_event_obj(eventKey)
        event_alliance = event_dictionary['alliances'][number - 1]
        return event_alliance

    def get_event_alliance_members(self, eventKey, number): #Returns json array of alliance members in event from event key and alliance seed
        event_dictionary = self.get_event_obj(eventKey)
        event_alliance_picks = event_dictionary['alliances'][number - 1]['picks']
        return event_alliance_picks

    def get_event_alliance_declines(self, eventKey, number): #Returns json array of alliance declines in event from event key and alliance seed
        event_dictionary = self.get_event_obj(eventKey)
        event_alliance_declines = event_dictionary['alliances'][number - 1]['declines']
        return event_alliance_declines

    def get_event_type_string(self, eventKey): #Returns event type string from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_type_string = event_dictionary['event_type_string']
        return event_type_string

    def get_event_start_date(self, eventKey): #Returns event start date from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_start_date = event_dictionary['start_date']
        return event_start_date

    def get_event_event_type(self, eventKey): #Returns event type int from event key
        event_dictionary = self.get_event_obj(eventKey)
        event_event_type = event_dictionary['event_type']
        return event_event_type
