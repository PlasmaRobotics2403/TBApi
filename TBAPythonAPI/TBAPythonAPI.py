import os
import sys
import requests

class TBAParser:
  def __init__(self, teamNumber, packageID, versionID):
    self.teamNumber = teamNumber
    self.packageID = packageID
    self.versionID = versionID
    self.header = {'X-TBA-App-Id': 'frc{team}:{package}:{version}'.format(team = teamNumber, package = packageID, version = versionID)}
    self.baseURL = 'http://www.thebluealliance.com/api/v2/'

  #Team Info
  
  def get_team_obj(self, teamNumber):
    
    request = (self.baseURL + /team/frc + teamNumber)
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
