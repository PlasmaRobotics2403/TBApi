import os
import sys
import requests

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
        response = requests.get(request, headers=header)
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
