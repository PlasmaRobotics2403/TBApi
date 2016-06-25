#BLUE ALLIANCE API FOR PYTHON
import os
import sys
import requests
import datetime

class TBATeam:
    def __init__(self, raw_json):
        self.raw = raw_json
        self.website = raw_json['website']
        self.name = raw_json['name']
        self.locality = raw_json['locality']
        self.region = raw_json['region']
        self.country_name = raw_json['country_name']
        self.location = raw_json['location']
        self.team_number = raw_json['team_number']
        self.key = raw_json['key']
        self.nickname = raw_json['nickname']
        self.rookie_year = raw_json['rookie_year']
        self.motto = raw_json['motto']

class TBAEvent:
    def __init__(self, raw_json):
        self.raw = raw_json
        self.key = raw_json['key']
        self.website = raw_json['website']
        self.official = raw_json['official']
        self.end_date = raw_json['end_date']
        self.name = raw_json['name']
        self.short_name = raw_json['short_name']
        self.facebook_eid = raw_json['facebook_eid']
        self.event_district_string = raw_json['event_district_string']
        self.venue_address = raw_json['venue_address']
        self.event_district = raw_json['event_district']
        self.location = raw_json['location']
        self.event_code = raw_json['event_code']
        self.year = raw_json['year']
        self.webcast = raw_json['webcast']
        self.timezone = raw_json['timezone']
        self.alliances = raw_json['alliances']
        self.event_type_string = raw_json['event_type_string']
        self.start_date = raw_json['start_date']
        self.event_type = raw_json['event_type']

class TBAMatch:
    def __init__(self, raw_json):
        self.raw = raw_json
        self.comp_level = raw_json['comp_level']
        self.match_number = raw_json['match_number']
        self.number = raw_json['match_number']
        self.videos = raw_json['videos']
        self.time_string = raw_json['time_string']
        self.set_number = raw_json['set_number']
        self.key = raw_json['key']
        self.time = raw_json['time']
        self.score_breakdown = raw_json['score_breakdown']
        self.alliances = raw_json['alliances']
        self.event_key = raw_json['event_key']

class TBAAward:
    def __init__(self, raw_json):
        self.raw = raw_json
        self.event_key = raw_json['event_key']
        self.award_type = raw_json['award_type']
        self.type = raw_json['award_type']
        self.name = raw_json['name']
        self.recipient_list = raw_json['recipient_list']
        self.year = raw_json['year']

class TBAMedia:
    def __init__(self, raw_json):
        self.raw = raw_json
        self.type = raw_json['type']
        self.details = raw_json['details']
        self.foreign_key = raw_json['foreign_key']

class TBARobotGroup:
    def __init__(self, raw_json):
        self.raw = raw_json

    def get_year(self, year):
        year_json = self.raw[str(year)]
        year_obj = TBARobot(year_json)

        return year_obj

class TBARobot:
    def __init__(self, raw_json):
        self.raw = raw_json
        self.team_key = raw_json['team_key']
        self.name = raw_json['name']
        self.key = raw_json['key']
        self.year = raw_json['year']


class TBAParser:
    def __init__(self, team_number, package_name, version_number):
        self.team_number = team_number
        self.package_name = package_name
        self.version_number = version_number
        self.header = {'X-TBA-App-Id': 'frc{team}:{package}:{version}'.format(team = team_number, package = package_name, version = version_number)}
        self.baseURL = 'http://www.thebluealliance.com/api/v2'

    def __pull_team_list_by_page(self, page): #Helper function to make code for get_team_list simpler.
        request = (self.baseURL + "/teams/" + str(page))
        response = requests.get(request, headers = self.header)
        json_list = response.json()
        team_list = []

        for team in json_list:
            team_obj = TBATeam(team)
            team_list = team_list + [team_obj]

        return team_list

    def get_team_list(self, page = None): #get list of FRC teams' TBATeam objects, either the entire list, or by page #
        if not page is None:
            team_list = self.__pull_team_list_by_page
        else:
            team_list = []

            for page in range(0,100): #Allows for significant team-expansion (up to 55000 FRC teams).  At that point in time, we will probably be on APIv3 or more.
                partial_list = self.__pull_team_list_by_page(page)

                try:
                    if not partial_list[0] is None:
                        team_list = team_list + partial_list #combine partial with previously set up 'full' list to grow list as we iterate over the range of pages
                    else:
                        break #kill loop once we hit NULL data
                except:
                    break #kill loop once we hit NULL data

        return team_list

    def get_team(self, team_key): #get a team's TBATeam object
        request = (self.baseURL + "/team/" + team_key)
        response = requests.get(request, headers = self.header)
        json = response.json()
        team_object = TBATeam(json)

        return team_object

    def __pull_team_events(self, team_key, year):
        request = (self.baseURL + "/team/" + team_key + "/" + str(year) + "/events")
        response = requests.get(request, headers = self.header)
        json = response.json()
        event_list = []

        for event in json:
            event_obj = TBAEvent(event)
            event_list = event_list + [event_obj]

        return event_list

    def __pull_all_team_events(self, team_key):
        request = (self.baseURL + "/team/" + team_key + "/history/events")
        response = requests.get(request, headers = self.header)
        json = response.json()
        event_list = []

        for event in json:
            event_obj = TBAEvent(event)
            event_list = event_list + [event_obj]

        return event_list

    def get_team_events(self, team_key, year=None):
        if not year is None:
            event_list = self.__pull_team_events(team_key, year)
        else:
            event_list = self.__pull_all_team_events(team_key)
        return event_list

    def get_team_event_awards(self, team_key, event_key):
        request = (self.baseURL + "/team/" + team_key + "/event/" + event_key + "/awards")
        response = requests.get(request, headers = self.header)
        json = response.json()
        award_list = []

        for award in json:
            award_obj = TBAAward(award)
            award_list = award_list + [award_obj]

        return award_list

    def get_team_event_matches(self, team_key, event_key):
        request = (self.baseURL + "/team/" + team_key + "/event/" + event_key + "/matches")
        response = requests.get(request, headers = self.header)
        json = response.json()
        match_list = []

        for match in json:
            match_obj = TBAMatch(match)
            match_list = match_list + [match_obj]

        return match_list

    def __pull_team_media(self, team_key, year):
        request = (self.baseURL + "/team/" + team_key + "/" + str(year) + "/media")
        response = requests.get(request, headers = self.header)
        json = response.json()
        media_list = []

        for media in json:
            media_obj = TBAMedia(media)
            media_list = media_list + [media_obj]

        return media_list

    def get_team_media(self, team_key, year = None):
        if not year is None:
            media_list = self.__pull_team_media(team_key, year)
        else:
            rookie_year = self.get_team(team_key).rookie_year
            current_year = datetime.datetime.now().year

            media_list = []

            for check_year in range(rookie_year, current_year):
                partial_list = self.__pull_team_media(team_key, check_year)
                media_list = media_list + partial_list

        return media_list

    def get_team_history_events(self, team_key):
        events_list = self.__pull_all_team_events(team_key)
        return events_list

    def get_team_history_awards(self, team_key):
        request = (self.baseURL + "/team/" + team_key + "/history/awards")
        response = requests.get(request, headers = self.header)
        json = response.json()
        award_list = []

        for award in json:
            award_obj = TBAAward(award)
            award_list = award_list + [award_obj]

        return award_list

    def get_team_history_robots(self, team_key):
        request = (self.baseURL + "/team/" + team_key + "/history/robots")
        response = requests.get(request, headers = self.header)
        json = response.json()

        robo_container_obj = TBARobotGroup(json)

        return robo_container_obj

    def get_event_list(self, year):
        request = (self.baseURL + "/events/" + str(year))
        response = requests.get(request, headers = self.header)
        json = response.json()
        event_list = []

        for event in json:
            event_obj = TBAEvent(event)
            event_list = event_list + [event_obj]

        return event_list

    def get_event(self, event_key):
        request = (self.baseURL + "/event/" + event_key)
        response = requests.get(request, headers = self.header)
        json = response.json()

        event_obj = TBAEvent(json)

        return event_obj

    def get_event_teams(self, event_key):
        request = (self.baseURL + "/event/" + event_key + "/teams")
        response = requests.get(request, headers = self.header)
        json = response.json()

        team_list = []

        for team in json:
            team_obj = TBATeam(team)
            team_list = team_list + [team_obj]

        return team_list

    def get_event_matches(self, event_key):
        request = (self.baseURL + "/event" + event_key + "/matches")
        response = requests.get(request, headers = self.header)
        json = response.json()

        match_list = []

        for match in json:
            match_obj = TBAMatch(match)
            match_list = match_list + [match_obj]

        return match_list
