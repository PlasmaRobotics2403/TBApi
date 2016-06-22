class TBA_Team:
    def __init__(self, rawJSON):
        self.raw = rawJSON

class TBA_Event:
    def __init__(self, rawJSON):
        self.raw = rawJSON

class TBA_Match:
    def __init__(self, rawJSON):
        self.raw = rawJSON

class TBA_Award:
    def __init__(self, rawJSON):
        self.raw = rawJSON

class TBA_Media:
    def __init__(self, rawJSON):
        self.raw = rawJSON

class TBA_Robot:
    def __init__(self, rawJSON):
        self.raw = rawJSON

class TBAParser:
    def __init__(self, teamNumber, packageID, versionID):
        self.teamNumber = teamNumber
        self.packageID = packageID
        self.versionID = versionID
        self.header = {'X-TBA-App-Id': 'frc{team}:{package}:{version}'.format(team = teamNumber, package = packageID, version = versionID)}
        self.baseURL = 'http://www.thebluealliance.com/api/v2'
