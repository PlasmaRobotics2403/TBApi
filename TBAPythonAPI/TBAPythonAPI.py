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

    def get_team_obj(self, teamNumber):

        request = (self.baseURL + "/team/frc" + teamNumber)
        response = requests.get(myRequest, headers=header)
        dictionary = response.json()

        return dictionary

    def get_team_full_name(self, teamNumber):
        team_dictionary = get_team_obj(teamNumber)
        full_name = team_dictionary['name']
        return full_name

    def get_team_nick_name(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        nick_name = team_dictionary['nickname']
        return nick_name

    def get_team_number(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        team_number = team_dictionary['team_number']
        return team_number

    def get_team_rookie_year(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        rookie_year = team_dictionary['rookie_year']
        return rookie_year

    def get_team_website(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        website = team_dictionary['rookie_year']
        return website

    def get_team_city(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        city = team_dictionary['locality']
        return city

    def get_team_region(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        region = team_dictionary['region']
        return region

    def get_team_location(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        location = team_dictionary['location']
        return location

    def get_team_key(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        key = team_dictionary['key']
        return key

    def get_team_country(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        country = team_dictionary['country_name']
        return country

    def get_team_motto(self, teamNumber):
        team_dictionary = getTeamObj(teamNumber)
        motto = team_dictionary['motto']
        return motto
