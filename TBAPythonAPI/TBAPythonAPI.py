import os
import sys
import requests

class TBAParser:
  def __init__(self, teamNumber, packageID, versionID)
    self.teamNumber = teamNumber
    self.packageID = packageID
    self.versionID = versionID
    self.header = {'X-TBA-App-Id': 'frc{team}:{package}:{version}'.format(team = teamNumber, package = packageID, version = versionID)}
    self.baseURL = 'http://www.thebluealliance.com/api/v2/'
