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
        self.name = raw_json['name']
        self.recipient_list = raw_json['recipient_list']
        self.year = raw_json['year']

class TBAMedia:
    def __init__(self, raw_json):
        self.raw = raw_json
        self.type = raw_json['type']
        self.details = raw_json['details']
        self.foreign_key = raw_json['foreign_key']

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
