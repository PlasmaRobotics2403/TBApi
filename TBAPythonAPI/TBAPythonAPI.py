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

    def get_team_obj(self, teamNumber):

        request = (self.baseURL + "/team/frc" + str(teamNumber))
        response = requests.get(request, headers = self.header)
        dictionary = response.json()
        return dictionary

    def get_team_full_name(self, teamNumber):
        team_dictionary = self.get_team_obj(teamNumber)
        full_name = team_dictionary['name']
        return full_name

    def get_team_nick_name(self, teamNumber):
        team_dictionary = self.get_team_obj(teamNumber)
        nick_name = team_dictionary['nickname']
        return nick_name


    #Event Info

    def get_event_obj(self, eventKey):
        request = (self.baseURL + "/event/" + eventKey)
        response = requests.get(request, headers = self.header)
        dictionary = response.json()
        return dictionary

    def get_event_key(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_key = event_dictionary['key']
        return event_key

    def get_event_website(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_website = event_dictionary['website']
        return event_website

    def get_event_is_official(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_is_official = event_dictionary['official']
        return event_is_official

    def get_event_end_date(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_end_date = event_dictionary['end_date']
        return event_end_date

    def get_event_name(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_name = event_dictionary['name']
        return event_name

    def get_event_short_name(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_short_name = event_dictionary['short_name']
        return event_short_name

    def get_event_facebook_eid(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_facebook_eid = event_dictionary['facebook_eid']
        return event_facebook_eid

    def get_event_district_string(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_district_string = event_dictionary['event_district_string']
        return event_district_string

    def get_event_venue_address(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_venue_address = event_dictionary['venue_address']
        return event_venue_address

    def get_event_district(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_district = event_dictionary['event_district']
        return event_district

    def get_event_location(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_location = event_dictionary['location']
        return event_location

    def get_event_code(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_code = event_dictionary['event_code']
        return event_code

    def get_event_year(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_year = event_dictionary['year']
        return event_year

    def get_event_webcast(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_webcast = event_dictionary['webcast']
        return event_webcast

    def get_event_timezone(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_timezone = event_dictionary['timezone']
        return event_timezone

    def get_event_alliances(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_alliances = event_dictionary['alliances']
        return event_alliances

    def get_event_alliance(self, eventKey, number):
        event_dictionary = self.get_event_obj(eventKey)
        event_alliance = event_dictionary['alliances'][number - 1]
        return event_alliance

    def get_event_alliance_members(self, eventKey, number):
        event_dictionary = self.get_event_obj(eventKey)
        event_alliance_picks = event_dictionary['alliances'][number - 1]['picks']
        return event_alliance_picks

    def get_event_alliance_declines(self, eventKey, number):
        event_dictionary = self.get_event_obj(eventKey)
        event_alliance_declines = event_dictionary['alliances'][number - 1]['declines']
        return event_alliance_declines

    def get_event_type_string(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_type_string = event_dictionary['event_type_string']
        return event_type_string

    def get_event_start_date(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_start_date = event_dictionary['start_date']
        return event_start_date

    def get_event_event_type(self, eventKey):
        event_dictionary = self.get_event_obj(eventKey)
        event_event_type = event_dictionary['event_type']
        return event_event_type
