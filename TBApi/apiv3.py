"""TBApi - Python Library for The Blue Alliance API v3"""

import os
import sys
import json
import datetime
import requests
from SQLiteHelper import SQLiteHelper as sq # SQLite3 Wrapper for easier reading and programming
import numpy as np
from numpy import array as np_array


# EXCEPTION: Data Class is EMPTY
class EmptyError(Exception):
    """EXCEPTION: Data Class is EMPTY."""
    def __init__(self):
        Exception.__init__(self, 'Data Class is EMPTY.')


# EXCEPTION: Data Class errored during data parsing
class ParseError(Exception):
    """EXCEPTION: Data Class errored during data parsing."""
    def __init__(self):
        Exception.__init__(self, 'Data Class errored during data parsing.')


# EXCEPTION: Impropper Key passed during data parsing
class KeyInputError(Exception):
    """EXCEPTION: Impropper Key passed during data parsing."""
    def __init__(self):
        Exception.__init__(self, 'Impropper Key passed during data parsing.')


# EXCEPTION: Network Connection to The Blue Alliance is Offline
class OfflineError(Exception):
    """EXCEPTION: Network Conenction to The Blue Alliance is Offline."""
    def __init__(self):
        Exception.__init__(self, 'Network Connection to The Blue Alliance is Offline.')


# List-Extension Class:  Adds extra functionality to lists used for data-returns
class DataList(list):
    """List-Extension used for storing data objects with extra information."""
    def __init__(self, data_list, json_array, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.extend(data_list)
        self.raw = json_array

        self.is_error = False

        if 'error' in json_array:
            if json_array['error'] is True:
                self.is_error = True

    # A method allowing for end-users to filter data-points by specific attributes, ex: team number.
    def filter(self, attr_name, attr_value):
        """Filter the stored objects by a given attribute.  Returns a new DataList."""

        return_list = self.__class__([], [])

        for data_object in self:
            desired_attribute = getattr(data_object, str(attr_name), None)

            if str(desired_attribute).lower() == str(attr_value).lower():
                return_list.append(data_object)
                return_list.raw.append(data_object.raw)

        return return_list

    # Customize Object Description Output to identify the given list as a DataList
    def __repr__(self):
        """Return a customized object description identifying the list as a DataList."""
        list_return = super().__repr__()
        return '<tbapi:DataList> {}'.format(list_return)

    # A method to return the standard Object Description Output if needed by the user
    @property
    def list_representation(self):
        """Return a JSON-like representation of the data in the list."""
        return super().__repr__()


# Basic Data Class:  Stores information about data returned by TBA by the parser.
class Data(object):
    """Base Data Class:  Meant for extension by base data models."""
    def __init__(self, json_array, identifier='Generic Data Object'):
        self.raw = json_array
        self.identifier = identifier

    # When referenced in terminal without called attribute, identify as a Data object
    def __repr__(self):
        """Return the Team Key Nickname as the Object Description"""
        return '<tbapi.Data: {}>'.format(self.identifier)


# Team Data Class: Provides team information returned by TBA by the parser.
class Team(Data):
    """Team Data Class: Provides information regarding a given team."""

    @property
    def key(self):
        """Team Key of the represented team"""
        return self.raw['key']

    @property
    def team_number(self):
        """Team Number of the represented team"""
        return self.raw['team_number']

    @property
    def number(self):
        """Team Number of the represented team"""
        return self.raw['team_number']

    @property
    def nickname(self):
        """Nickname of the represented team"""
        return self.raw['nickname']

    @property
    def nick(self):
        """Nickname of the represented team"""
        return self.raw['nickname']

    @property
    def name(self):
        """Full Name of the represented team"""
        return self.raw['name']

    @property
    def rookie_year(self):
        """Rookie Year of the represented team"""
        return self.raw['rookie_year']

    @property
    def motto(self):
        """Motto of the represented team"""
        return self.raw['motto']

    @property
    def website(self):
        """Website URL for the represented team"""
        return self.raw['website']

    @property
    def address(self):
        """Address of the represented team"""
        return self.raw['address']

    @property
    def city(self):
        """Home City of the represented team"""
        return self.raw['city']

    @property
    def state(self):
        """State or Province of the represented team"""
        return self.raw['state_prov']

    @property
    def state_prov(self):
        """State or Province of the represented team"""
        return self.raw['state_prov']

    @property
    def province(self):
        """State or Province of the represented team"""
        return self.raw['state_prov']

    @property
    def country(self):
        """Home Country of the represented team"""
        return self.raw['country']

    @property
    def postal_code(self):
        """Postal Code of the represented team"""
        return self.raw['postal_code']

    @property
    def location_name(self):
        """Name of the location of the represented team"""
        return self.raw['location_name']

    @property
    def lat(self):
        """Latitude of the represented team"""
        return self.raw['lat']

    @property
    def latitude(self):
        """Latitude of the represented team"""
        return self.raw['lat']

    @property
    def lng(self):
        """Longitude of the represented team"""
        return self.raw['lng']

    @property
    def longitude(self):
        """Longitude of the represented team"""
        return self.raw['lng']

    @property
    def home_championship(self):
        """Dictionary sorted by year containing the home championship of the represented team"""
        return self.raw['home_championship']

    @property
    def gmaps_place_id(self):
        """Place ID of the represented team as registered in Google Maps"""
        return self.raw['gmaps_place_id']

    @property
    def gmaps_url(self):
        """A URL representing the location of the represented team in Google Maps"""
        return self.raw['gmaps_url']

    # When referenced in terminal without called attribute, output team_number & nick (readability)
    def __repr__(self):
        """Return the Team Key Nickname as the Object Description"""
        return '<tbapi.Team: {} - {}>'.format(self.team_number, self.nickname)

    # When converted to a string, return the team key
    def __str__(self):
        """Return the Team Key when converted to a String."""
        return self.key

    # When converted to an integer, return the team_number
    def __int__(self):
        """Return the Team Number when converted to an integer."""
        return int(self.team_number) # Convert to an integer, in case of errors in JSON parsing.


# District Data Class: Provides information about a given district.
class District(Data):
    """District Data Class: Provides information regarding a given district."""

    @property
    def key(self):
        """The key of the represented district."""
        return self.raw['key']

    @property
    def year(self):
        """The year of operation of the represented district."""
        return self.raw['year']

    @property
    def display_name(self):
        """A string representing a human readable name for the represented district."""
        return self.raw['display_name']

    @property
    def abbreviation(self):
        """A string representing a simple abbreviation of the represented district's name."""
        return self.raw['abbreviation']

    # When referenced in terminal without called attribute, output display_name, year, and key (readability).
    def __repr__(self):
        """Return the Team Key and Team Name as the Object Description."""
        return '<tbapi.District: {} {} District ({})>'.format(self.year, self.display_name, self.key)

    # When converted to a string, return the district key
    def __str__(self):
        """Return the District Key when converted to a String."""
        return self.key

    # When converted to an integer, return the district year
    def __int__(self):
        """Return the district year when converted to an Integer."""
        return int(self.year) # Convert to an integer, in case of errors in JSON parsing.


# Robot Data Class: Provides information about an individual robot beloging to a team in a given year.
class Robot(Data):
    """Robot Data Class: Provides information about a robot belonging to a team in a given year."""

    @property
    def key(self):
        """The key of the represented robot."""
        return self.raw['key']

    @property
    def robot_name(self):
        """The name of the represented robot."""
        return self.raw['robot_name']

    @property
    def name(self):
        """The name of the represented robot."""
        return self.raw['robot_name']

    @property
    def team_key(self):
        """The team_key of the team that owns the represented robot."""
        return self.raw['team_key']

    @property
    def team(self):
        """The team_key of the team that owns the represented robot."""
        return self.raw['team_key']

    @property
    def team_number(self):
        """The team_number of the team that owns the represented robot."""
        return self.raw['team_key'][3:]

    @property
    def year(self):
        """The year in which the represented robot was built and competed."""
        return self.raw['year']

    # When referenced in terminal without called attribute, output robot_name and key (readability).
    def __repr__(self):
        """Return the Robot Name and Key when referenced."""
        return '<tbapi.Robot: {} ({})>'.format(self.robot_name, self.key)

    # When converted to a string, return the robot's key.
    def __str__(self):
        """Return the Robot Key when converted to a String."""
        return self.key

    # When converted to an integer, return the year in which the robot was built.
    def __int__(self):
        """Return the robot build year when converted to an Integer."""
        return int(self.year) # Convert to an integer, in case of errors in JSON parsing.


# Cache Database Defaults Class: Used for setting up default columns in the cache database.
class CacheTable(object):
    """Database Cache Defaults:  Holds default cache table column information."""
    def __init__(self):
        self.columns = ['REQUEST', 'RESPONSE', 'REQUESTED', 'LAST_MODIFIED', 'MAX_AGE']
        self.datatypes = ['TEXT PRIMARY KEY NOT NULL', 'TEXT NOT NULL', 'TEXT NOT NULL', 'TEXT NOT NULL', 'TEXT NOT NULL']
        self.seed = []


# Main Parser Class:  All requests routed through this class's methods.
class Parser:
    """TBA Parser Class:  Routes API requests and handles caching. Requires v3 API Key from TBA."""

    # Initiate Information needed for connection to TBA v3 (api_key)
    def __init__(self, api_key, *, cache=True, force_cache=False, log_cache=False):
        self.api_key = api_key # TBA API v3 API key 
        self.cache = cache
        self.force_cache = force_cache
        self.log_cache = log_cache
        self.base_url = 'http://www.thebluealliance.com/api/v3'

        if self.cache:
            self.storage_path = os.path.dirname(sys.executable) + '/.tbapi'

            if not os.path.exists(self.storage_path):
                try:
                    os.makedirs(self.storage_path)
                except:
                    self.storage_path = os.getcwd()

            self.cache_db = sq.Connect(self.storage_path + '/cache')

            if not self.cache_db.table('cache_data').tableExists():
                cache_preset = CacheTable()
                self.cache_db.table('cache_data').init(cache_preset)

    # Method to pull JSON array from TBA v3 API.  Includes Caching and Offline Support.
    def pull_response_json(self, path, *, force_new=False, force_cache=False, log_cache=False):
        """Pull the JSON response to a given path from the TBA API servers or the response cache."""

        current_time = datetime.datetime.now() # Get the Current Time at the start of method execution

        if self.cache and force_new == False: # If caching is enabled, and a new response is not forced, attempt pulling from cache

            cache_reply = self.cache_db.table('cache_data').select('RESPONSE', 'REQUESTED', 'LAST_MODIFIED', 'MAX_AGE').where('REQUEST').equals(path).execute() # Query Cache Database for last stored response

            # Default Values
            cache_response = None
            cache_requested = None
            cache_last_modified = None
            cache_last_modified_str = ''
            cache_max_age = ''

            # Pull Data from Database:  Queried Variable is primary key, so only one row is possible.
            for entry in cache_reply:
                cache_response = json.loads(entry[0]) # Convert stored response back to Python Dictionaries and Lists
                cache_requested = datetime.datetime.strptime(entry[1].strip(), '%a, %d %b %Y %H:%M:%S') # Convert Strings to Datetime objects
                cache_last_modified = datetime.datetime.strptime(entry[2].strip(), '%a, %d %b %Y %H:%M:%S %Z') # Convert Strings to Datetime objects
                cache_last_modified_str = entry[2]
                cache_max_age = entry[3]

            if not cache_response is None: # If Database Response NOT blank:  AKA, if database value for given path not null
                request = (self.base_url + path) # Full Request URL generation based on base_url as set in __init__
                header = {'X-TBA-Auth-Key': self.api_key, 'If-Modified-Since': cache_last_modified_str} # Form headers, but substitute in last_modified string from database to see if data has changed since last database pull.

                if force_cache or self.force_cache:
                    if self.log_cache or log_cache:
                        print('Forcing Read from Cache...')

                    if cache_response == []:
                        raise EmptyError

                    return cache_response

                try:
                    response = requests.get(request, headers=header)
                except:
                    cache_expire = cache_requested + datetime.timedelta(seconds=int(cache_max_age))

                    if current_time <= cache_expire:
                        if self.log_cache or log_cache:
                            print('Offline: Reading from Cache...')

                        if cache_response == []:
                            raise EmptyError

                        return cache_response
                    else:
                        raise OfflineError

                if response.status_code == 304:
                    if self.log_cache or log_cache:
                        print('304 NOT MODIFIED: Reading from Cache...')

                    if cache_response == []:
                        raise EmptyError

                    return cache_response
                else:
                    if self.log_cache or log_cache:
                        print('Data Modified, Ignoring Cache...')

                    try:
                        json_array = response.json()
                    except:
                        raise ParseError

                    response_string = json.dumps(json_array)
                    response_headers = response.headers
                    response_last_modified = response_headers['Last-Modified']
                    response_cache_control = response_headers['Cache-Control']
                    current_time_str = current_time.strftime('%a, %d %b %Y %H:%M:%S')

                    response_max_age = ''
                    cache_control_array = response_cache_control.split(',')

                    for cache_control_item in cache_control_array:
                        cache_control_item = cache_control_item.strip()
                        if cache_control_item.startswith('max-age='):
                            response_max_age = cache_control_item.strip()[8:]

                    self.cache_db.table('cache_data').update('RESPONSE', 'REQUESTED', 'LAST_MODIFIED', 'MAX_AGE').insert(response_string, current_time_str, response_last_modified, response_max_age).where('REQUEST').equals(path).execute()

                    if json_array == []:
                        raise EmptyError

                    return json_array

        request = (self.base_url + path)
        header = {'X-TBA-Auth-Key': self.api_key}

        try:
            response = requests.get(request, headers=header)

            if self.log_cache or log_cache:
                print('No Cache Available, Pulling New Data...')
        except:
            raise OfflineError

        try:
            json_array = response.json()
        except:
            raise ParseError

        if self.cache:
            response_string = json.dumps(json_array)
            response_headers = response.headers
            last_modified = response_headers['Last-Modified']
            cache_control = response_headers['Cache-Control']
            current_time_str = current_time.strftime('%a, %d %b %Y %H:%M:%S')

            response_max_age = ''
            cache_control_array = cache_control.split(',')

            for cache_control_item in cache_control_array:
                cache_control_item = cache_control_item.strip()
                if cache_control_item.startswith('max-age='):
                    response_max_age = cache_control_item.strip()[8:]

            self.cache_db.table('cache_data').insert(path, response_string, current_time_str, last_modified, response_max_age).into('REQUEST', 'RESPONSE', 'REQUESTED', 'LAST_MODIFIED', 'MAX_AGE')

        if json.dumps(json_array) == '[]':
            raise EmptyError

        return json_array


    ### CALL METHODS
    # Get a List of FRC Teams
    def get_team_list(self, *, page=None, year=None, force_new=False, force_cache=False, log_cache=False):
        """Get a list of teams.  'page' and 'year' values optional."""
        if not page is None:
            return self.__get_team_list_page(page, year=year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        else:
            team_list = DataList([], [])

            for prospective_page in range(0,100):
                try:
                    partial_list = self.__get_team_list_page(prospective_page, year=year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
                except EmptyError:
                    break

                team_list += partial_list
                team_list.raw += partial_list.raw

        return team_list

    # HELPER: get single page of team data
    def __get_team_list_page(self, page, *, year=None, force_new=False, force_cache=False, log_cache=False):
        """HELPER METHOD: Get a single page of teams."""
        return_array = self.pull_response_json('/teams/{}{}'.format('{}/'.format(year) if not year is None else '', str(page)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)

        page_list = DataList([], return_array)

        for item in return_array:
            team_obj = Team(item)
            page_list.append(team_obj)

        return page_list

    # Get a List of FRC Team Keys
    def get_team_key_list(self, *, page=None, year=None, force_new=False, force_cache=False, log_cache=False):
        """Get a list of team keys.  'page' and 'year' values optional."""
        if not page is None:
            return self.__get_team_list_page(page, year=year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        else:
            key_list = []

            for prospective_page in range(0,100):
                try:
                    partial_list = self.__get_team_key_list_page(prospective_page, year=year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
                except EmptyError:
                    break

                key_list += partial_list

        return key_list
    
    # HELPER: get single page of team keys
    def __get_team_key_list_page(self, page, *, year=None, force_new=False, force_cache=False, log_cache=False):
        """HELPER METHOD: Get a single page of team keys."""
        return self.pull_response_json('/teams/{}{}/keys'.format('{}/'.format(year) if not year is None else '', str(page)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)


    # HELPER: convert team_number or team_key input to uniform team_key
    def __get_team_key(self, team_identifier):
        """Convert team_number or team_key to uniform team_key for request path generation."""
        if str(team_identifier).startswith('frc'):
            return team_identifier
        else:
            try:
                int(team_identifier)
            except ValueError:
                raise KeyInputError

            return 'frc' + str(team_identifier)

    # Get information about a single FRC Team by team number or team key
    def get_team(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a single team, by 'team_key' or 'team_number'."""
        return Team(self.pull_response_json('/team/{}'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache))

    # Get a list containing the years in which a given team has participated
    def get_team_years_participated(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list containing the years in which a given team has participated."""
        return self.pull_response_json('/team/{}/years_participated'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
    
    # Get a list of Districts that the given team has competed in
    def get_team_districts(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of districts in which the given team has competed in."""
        district_list = self.pull_response_json('/team/{}/districts'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([District(district_item) for district_item in district_list], district_list)

    # Get a list of Robots built and operated by a given team
    def get_team_robots(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of robots built and operated by a given team."""
        robot_list = self.pull_response_json('/team/{}/robots'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Robot(robot_item) for robot_item in robot_list], robot_list)