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


# EXCEPTION: Inpropper Key passed during data parsing
class KeyInputError(Exception):
    """EXCEPTION: Inpropper Key passed during data parsing."""
    def __init__(self):
        Exception.__init__(self, 'Inpropper Key passed during data parsing.')


# EXCEPTION: Network Connection to The Blue Alliance is Offline
class OfflineError(Exception):
    """EXCEPTION: Network Conenction to The Blue Alliance is Offline."""
    def __init__(self):
        Exception.__init__(self, 'Network Connection to The Blue Alliance is Offline.')


# EXCEPTION: Fluid Key not available
class FluidKeyError(Exception):
    """EXCEPTION: Fluid Key not available"""
    def __init__(self):
        Exception.__init__(self, 'Fluid Key not availble.  Key may not be available for the represented Season, if applicable.')


# List-Extension Class:  Adds extra functionality to lists used for data-returns
class DataList(list):
    """List-Extension used for storing data objects with extra information."""
    def __init__(self, data_list, json_array, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.extend(data_list)
        self.json_array = json_array

        self.is_error = False

        if 'error' in json_array:
            if json_array['error'] is True:
                self.is_error = True

    # A method allowing for end-users to filter data-points by specific attributes, ex: team number.
    def filter(self, attr_name, attr_value):
        """Filter the stored objects by a given attribute with a given value.

        Returns new DataList containing only Data Objects with attribute ``attr_name`` containing ``attr_value``."""

        return_list = self.__class__([], [])

        for data_object in self:
            actual_attribute = getattr(data_object, str(attr_name), None)

            if str(attr_value).lower() in str(actual_attribute).lower():
                return_list.append(data_object)
                return_list.raw.append(dict(data_object))

        return return_list

    # Return the raw JSON array used to create the list and it's contained Data objects.
    @property
    def raw(self):
        """Returns the raw JSON array used to create the :class:`DataList` object and it's contained :class:`Data` objects.

        Alias: *json_array* (modifiable dictionary available for concatenation or modification)"""
        return self.json_array

    # Customize Object Description Output to identify the given list as a DataList
    def __repr__(self):
        """Return a customized object description identifying the list as a DataList."""
        list_return = super().__repr__()
        return '<tbapi.DataList> {}'.format(list_return)

    # A method to return the standard Object Description Output if needed by the user
    @property
    def __representation(self):
        """Return a JSON-like string representation of the data in the list."""
        return super().__repr__()


# Basic Data Class:  Stores information about data returned by TBA by the parser.
class Data(dict):
    """Basic Data Class, extended with attributes for other Data Models.

    All :class:`Data` objects are extensions of the :class:`dict` class, meaning that the raw JSON used to create these objects can be obtained by treating the object as a dictionary rather than an object.

    :class:`Data` objects maintain a reference to the :class:`Parser` object that created them in order to live pull further information later on down the road.

    .. warning::
        When treating :class:`Data` objects as dictionaries, all data is returned "as-is" by TBA.  No futher processing is done to transform second-level dictionaries into their own :class:`Data` objects."""
    def __init__(self, json_array, parser, options=None):
        self.update(json_array)
        self.parser = parser

        if not options == None:
            self.options = options
        else:
            self.options = {'force_new':False, 'force_cache':False, 'log_cache':False}

    # When referenced in terminal without called attribute, identify as a Data object
    def __repr__(self):
        """Return a modified object Description for more useful identification in the console."""
        return '<tbapi.Data: Custon Data Object>'


# Status Data Class: Represents the Status of The Blue Alliance API v3.
class Status(Data):
    """Status Data Class: Represents the Status of The Blue Alliance API v3 and it's associated applications."""

    @property
    def android(self):
        """:class:`App`: Android App Status information."""
        modified_dict = self['android']
        modified_dict['platform'] = 'Android'
        return App(modified_dict)

    @property
    def ios(self):
        """:class:`App`: iOS App Status Information"""
        modified_dict = self['ios']
        modified_dict['platform'] = 'iOS'
        return App(modified_dict)

    @property
    def current_season(self):
        """The Current FIRST Robotics Competition Season."""
        return self['current_season']

    @property
    def max_season(self):
        """The maximum FIRST Robotics Competition Season."""
        return self['max_season']

    @property
    def is_datafeed_down(self):
        """A Boolean representing whether or not the datafeed is down."""
        return bool(self['is_datafeed_down'])

    @property
    def down_events(self):
        """A raw JSON array representing events that are currently down."""
        return self['down_events']

    def __repr__(self):
        """Modified Reference Return"""
        return '<tbapi.Status: API Status Keys>'


# App Data Class: Represents TBA Mobile App Information.
class App(Data):
    """App Data Class: Represents TBA Mobile App Information."""

    @property
    def latest_app_version(self):
        """The Latest Available App Version on the represented Platform.

            Alias: *latest*"""
        return self['latest_app_version']

    @property
    def latest(self):
        return self['latest_app_version']

    @property
    def min_app_version(self):
        """The Minimum Supported  App Version on the represented Platform.

            Alias: *minimum*, *min*"""
        return self['min_app_version']

    @property
    def minimum(self):
        return self['min_app_version']

    @property
    def min(self):
        return self['min_app_version']

    # When referenced in terminal without called attribute, identify as a Data object
    def __repr__(self):
        """Return the Team Key Nickname as the Object Description"""
        return '<tbapi.App: {} Platform>'.format(self['platform'])


# Team Data Class: Provides team information returned by TBA by the parser.
class Team(Data):
    """Team Data Class: Provides information regarding a given team."""

    @property
    def key(self):
        """Team Key of the represented team."""
        return self['key']

    @property
    def team_number(self):
        """Team Number of the represented team.

        Alias: *number*"""
        return self['team_number']

    @property
    def number(self):
        return self['team_number']

    @property
    def nickname(self):
        """Nickname of the represented team.

        Alias: *nick*"""
        return self['nickname']

    @property
    def nick(self):
        return self['nickname']

    @property
    def name(self):
        """Full Name of the represented team"""
        return self['name']

    @property
    def rookie_year(self):
        """Rookie Year of the represented team"""
        return self['rookie_year']

    @property
    def motto(self):
        """Motto of the represented team"""
        return self['motto']

    @property
    def website(self):
        """Website URL for the represented team"""
        return self['website']

    @property
    def address(self):
        """Address of the represented team."""
        return self['address']

    @property
    def city(self):
        """Home City of the represented team."""
        return self['city']

    @property
    def state_prov(self):
        """State or Province of the represented team.

        Alias: *state*, *province*"""
        return self['state_prov']

    @property
    def state(self):
        return self['state_prov']

    @property
    def province(self):
        return self['state_prov']

    @property
    def country(self):
        """Home Country of the represented team."""
        return self['country']

    @property
    def postal_code(self):
        """Postal Code of the represented team."""
        return self['postal_code']

    @property
    def location_name(self):
        """Name of the location of the represented team."""
        return self['location_name']

    @property
    def lat(self):
        """Latitude of the represented team.

        Alias: *latitude*"""
        return self['lat']

    @property
    def latitude(self):
        return self['lat']

    @property
    def lng(self):
        """Longitude of the represented team.

        Alias: *longitude*"""
        return self['lng']

    @property
    def longitude(self):
        return self['lng']

    @property
    def home_championship(self):
        """Dictionary sorted by year containing the home championship of the represented team."""
        return self['home_championship']

    @property
    def gmaps_place_id(self):
        """Place ID of the represented team as registered in Google Maps."""
        return self['gmaps_place_id']

    @property
    def gmaps_url(self):
        """A URL representing the location of the represented team in Google Maps."""
        return self['gmaps_url']

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
        return self['key']

    @property
    def year(self):
        """The year of operation of the represented district."""
        return self['year']

    @property
    def display_name(self):
        """A string representing a human readable name for the represented district."""
        return self['display_name']

    @property
    def abbreviation(self):
        """A string representing a simple abbreviation of the represented district's name."""
        return self['abbreviation']

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
        return self['key']

    @property
    def robot_name(self):
        """The name of the represented robot."""
        return self['robot_name']

    @property
    def name(self):
        """The name of the represented robot."""
        return self['robot_name']

    @property
    def team_key(self):
        """The team_key of the team that owns the represented robot."""
        return self['team_key']

    @property
    def team(self):
        """:class:`Team`: The Team that owns the represented robot."""
        return self.parser.get_team(self['team_key'], force_new=self.options['force_new'], force_cache=self.options['force_cache'], log_cache=self.options['log_cache'])

    @property
    def team_number(self):
        """The team_number of the team that owns the represented robot."""
        return self['team_key'][3:]

    @property
    def year(self):
        """The year in which the represented robot was built and competed."""
        return self['year']

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


# Social Media Data Class: Represents a team's presense on a social media platform.
class Media(Data):
    """Media Data Class: Represents a team's presense on a social media platform."""

    @property
    def details(self):
        """Details about the represented Social Media Presense."""
        return self['details']

    @property
    def foreign_key(self):
        """Foreign Key for the represented Social Media Presense."""
        return self['foreign_key']

    @property
    def key(self):
        """Foreign Key for the represented Social Media Presense."""
        return self['foreign_key']

    @property
    def preferred(self):
        """Whether or not the given Social Media presense is "preferred" by its Team."""
        return self['preferred']

    @property
    def type(self):
        """The type of Social Media Presense represented."""
        return self['type']

    # When referenced in terminal without called attribute, output Robot Name and Key.
    def __repr__(self):
        """Return the Robot Name and Key when referenced."""
        return '<tbapi.Social: {}>'.format(self.type)


# Event Data Class: Represents a given event and it's corresponding data.
class Event(Data):
    """Event Data Class:  Represents a given Event and it's corresponding data."""

    @property
    def key(self):
        """The key for the represented event."""
        return self['key']

    @property
    def event_code(self):
        """The event code for the represented event."""
        return self['event_code']

    @property
    def code(self):
        """The event code for the represented event."""
        return self['event_code']

    @property
    def year(self):
        """The year in which the represented event takes place."""
        return self['year']

    @property
    def week(self):
        """The event week in which the represented event takes place."""
        return self['week']

    @property
    def name(self):
        """The name of the represented event."""
        return self['name']

    @property
    def short_name(self):
        """The short name of the represented event."""
        return self['short_name']

    @property
    def event_type(self):
        """The type of the represented event."""
        return self['event_type']

    @property
    def event_type_string(self):
        """A string representing the type of the represented event."""
        return self['event_type_string']

    @property
    def start_date(self):
        """The starting date of the represented event."""
        return self['start_date']

    @property
    def start(self):
        """The starting date of the represented event."""
        return self['start_date']

    @property
    def end_date(self):
        """The ending date of the represented event."""
        return self['end_date']

    @property
    def end(self):
        """The ending date of the represented event."""
        return self['end_date']

    @property
    def webcasts(self):
        """:class:`DataList`: A DataList of :class:`Webcast` objects for the represented event."""
        modified_return = self['webcasts']
        modified_return['event'] = '{} ({})'.format(self.name, self.key)
        return DataList([Webcast(webcast_item, self.parser, self.options) for webcast_item in modified_return], self['webcasts'])

    @property
    def website(self):
        """The Website for the represented event."""
        return self['website']

    @property
    def district(self):
        """:class:`District`: The District in which the represented event takes place, if available."""
        return District(self['district'], self.parser, self.options)

    @property
    def location_name(self):
        """The name of the location at which the represented event takes place."""
        return self['location_name']

    @property
    def lat(self):
        """A float representing the latitude of the represented event's venue."""
        return self['lat']

    @property
    def latitude(self):
        """A float representing the latitude of the represented event's venue."""
        return self['lat']

    @property
    def lng(self):
        """A float representing the latitude of the represented event's venue."""
        return self['lng']

    @property
    def longitude(self):
        """A float representing the longitude of the represented event's venue."""
        return self['lng']

    @property
    def address(self):
        """The address of the venue of the represented event."""
        return self['address']

    @property
    def city(self):
        """The city of the venue of the represented event."""
        return self['city']

    @property
    def state_prov(self):
        """The state or province of the venue of the represented event."""
        return self['state_prov']

    @property
    def state(self):
        """The state or province of the venue of the represented event."""
        return self['state_prov']

    @property
    def province(self):
        """The state or province of the venue of the represented event."""
        return self['state_prov']

    @property
    def country(self):
        """The country of the venue of the represented event."""
        return self['country']

    @property
    def postal_code(self):
        """The postal code of the venue of the represented event."""
        return self['postal_code']

    @property
    def timezone(self):
        """The timezone of the venue of the represented event."""
        return self['timezone']

    @property
    def gmaps_place_id(self):
        """The google maps place id of the venue of the represented event."""
        return self['gmaps_place_id']

    @property
    def gmaps_url(self):
        """The google maps url of the venue of the represented event."""
        return self['gmaps_url']

    @property
    def first_event_id(self):
        """I have no idea what this does."""
        return self['first_event_id']

    # When referenced in terminal without called attribute, output event name and key.
    def __repr__(self):
        """Return the Event Name and Key when referenced."""
        return '<tbapi.Event: {} ({})>'.format(self.name, self.key)


# EventStatus Data Class: Represents the status of a team at a given event.
class EventStatus(Data):
    """EventStatus Data Class: Represents the status of a team at a given event.

        TODO: Finish this data class and add object generation to :class:`Parser`"""

    @property
    def alliance(self):
        """:class:`TeamAlliance`: Basic information about the associated team's playoff alliance, if available."""
        if self['alliance'] != None:
            return TeamAlliance(self['alliance'], self.parser, self.options)
        else:
            return None

    @property
    def alliance_status_str(self):
        """String representing the alliance status of the associated team.

        Alias: *alliance_status*, *alliance_status_string*"""
        return self['alliance_status_str']

    @property
    def alliance_status_string(self):
        return self['alliance_status_str']

    @property
    def alliance_status(self):
        return self['alliance_status_str']

    @property
    def overall_status_str(self):
        """String representing the overall status of the associated team.

        Alias: *overall_status*, *overall_status_string*"""
        return self['overall_status_str']

    @property
    def overall_status_string(self):
        return self['overall_status_str']

    @property
    def overall_status(self):
        return self['overall_status_str']

    @property
    def playoff(self):
        """:class:`Playoff`: A team's status in the playoffs of the represented event."""
        return Playoff(self['playoff'], self.parser, self.options)

    @property
    def playoff_status_string(self):
        """A string representation of a team's status in the playoffs of the represented event.

        Alias: *playoff_status*"""
        return self['playoff_status_string']

    @property
    def playoff_status(self):
        return self['playoff_status_string']

    @property
    def qual(self):
        """:class:`Quals`: A team's status in the qualification rounds of the given event.

        Alias: *quals*"""
        return Quals(self['qual'], self.parser, self.options)

    @property
    def quals(self):
        return Quals(self['qual'], self.parser, self.options)

    # When referenced in terminal without called attribute, return modified response.
    def __repr__(self):
        """Modified Representation Response."""
        return '<tbapi.EventStats>'


# Playoff Data Class: Represents a team's status in the playoffs of an event.
class Playoff(Data):
    """Playoff Data Class:  Represents a team's status in the playoffs of a given Event."""

    @property
    def current_level_record(self):
        """:class:`Record`: The team's WLT Record at the current level.

        Alias: *level_record*"""
        return Record(self['current_level_record'], self.parser, self.options)

    @property
    def level_record(self):
        return self['current_level_record']

    @property
    def current_level(self):
        """The current level at which the team is competing within the playoffs.

        Alias: *level*"""
        return self['current_level']

    @property
    def level(self):
        return self['current_level']

    @property
    def playoff_average(self):
        """The average of the represented team during the playoffs.

        Alias: *average*"""
        return self['playoff_average']

    @property
    def average(self):
        return self['playoff_average']

    @property
    def record(self):
        """The Team's WLT Record in the playoffs."""
        return Record(self['record'], self.parser, self.options)

    @property
    def status(self):
        """The Team's Status in the Playoffs"""
        return self['status']

    # When referenced in terminal without called attribute, return modified response.
    def __repr__(self):
        """Modified Representation Response."""
        return '<tbapi.Playoff>'


# Quals Data Class:  Represents a team's status in the qualification rounds at a given event.
class Quals(Data):
    """Quals Data Class:  Represents a team's status in the qualification rounds at a given event."""

    @property
    def num_teams(self):
        """The number of teams that participated in the qualification rounds at a given event."""
        return self['num_teams']

    @property
    def ranking(self):
        """:class:`Ranking`: A representation of a team's Qualifications Ranking and the data used to calculate it."""
        self['ranking']['sort_order_info'] = self['sort_order_info']
        return QualsRanking(self['ranking'], self.parser, self.options)

    # When referenced in terminal without called attribute, return modified response.
    def __repr__(self):
        """Modified Representation Response."""
        return '<tbapi.Quals: Rank {}>'.format(str(self['ranking']['rank']))


class QualsRanking(Data):
    """QualsRanking Data Class:  Represents a team's rank in the qualification rounds at a given event."""

    @property
    def rank(self):
        """A Team's rank at a given event."""
        return self['rank']

    @property
    def record(self):
        """:class:`Record`: A Team's WLT Record in the qualification rounds at a given event."""
        return Record(self['record'], self.parser, self.options)

    @property
    def qual_average(self):
        """The Average of a team in the qualification rounds."""
        return self['qual_average']

    @property
    def matches_played(self):
        """The number of matches played by a team in the Qualification Rounds of the given event."""
        return self['matches_played']

    @property
    def dq(self):
        """The number of matches during which the given team was disqualified."""
        return self['dq'] 

    @property
    def team_key(self):
        """The `team_key` for the team represented by these data."""
        return self['team_key']

    @property
    def team(self):
        """:class:`Team`: The Team represented by these data."""
        return self.parser.get_team(self['team_key'], force_new=self.options['force_new'], force_cache=self.options['force_cache'], log_cache=self.options['log_cache'])


    # Return rank when converted to an integer
    def __int__(self):
        """Return rank when converted to an integer."""
        return int(self['rank'])

    # Return rank string when converted to an string
    def __str__(self):
        """Return rank string when converted to an string."""
        return 'Rank ' + str(self['rank'])

    # When referenced in terminal without called attribute, return modified response.
    def __repr__(self):
        """Modified Representation Response."""
        return '<tbapi.QualsRanking: Rank {}>'.format(str(self['rank']))


# Record Data Class: Represents a team's Win Loss Tie record at a given event or in a given level of an event.
class Record(Data):
    """Record Data Class: Represents a team's Win Loss Tie record at a given event or in a given level of an event."""

    @property
    def wins(self):
        """The number of won matches played by a given team in the represented level.

        Alias: *win*, *won*"""
        return self['wins']

    @property
    def win(self):
        return self['wins']

    @property
    def won(self):
        return self['wins']

    @property
    def losses(self):
        """The number of lost matches played by a given team in the represented level.

        Alias: *loss*, *lose*, *lost*"""
        return self['losses']

    @property
    def loss(self):
        return self['losses']

    @property
    def lose(self):
        return self['losses']

    @property
    def lost(self):
        return self['losses']

    @property
    def ties(self):
        """The number of won matches played by a given team in the represented level.

        Alias: *tie*, *tied*"""
        return self['ties']

    @property
    def tie(self):
        return self['ties']

    @property
    def tied(self):
        return self['ties']

    @property
    def string(self):
        """A String Representation of the given record in the W-L-T format."""
        return str(self['wins']) + '-' + str(self['losses']) + '-' + str(self['ties'])

    # When converted to a string, return a string representation in the W-L-T format.
    def __str__(self):
        """A String Representation of the given record in the W-L-T format."""
        return str(self['wins']) + '-' + str(self['losses']) + '-' + str(self['ties'])

    # When referenced in terminal without called attribute, return modified response.
    def __repr__(self):
        """Modified Representation Response."""
        return '<tbapi.Record>'

# Webcast Data Class: Represents a webcast for a given event and its corresponding data.
class Webcast(Data):
    """Webcast Data Class: Represents a webcast for a given event and its corresponding data."""

    @property
    def channel(self):
        """The Channel of the represented Webcast."""
        if 'channel' in self:
            return self['channel']
        else:
            return None

    @property
    def type(self):
        """The Type of the represented Webcast."""
        if 'type' in self:
            return self['type']
        else:
            return None

    @property
    def date(self):
        """The Date of the represented Webcast."""
        if 'date' in self:
            return self['date']
        else:
            return None

    @property
    def file(self):
        """The File of the represented Webcast."""
        if 'file' in self:
            return self['file']
        else:
            return None

    # When referenced in terminal without called attribute, output webcast information.
    def __repr__(self):
        """Return webcast information when referenced."""
        return '<tbapi.Webcast: Webcast for {}>'.format(self['event'])


# Video Data Class: Represents a video as posted on The Blue Alliance.
class Video(Data):
    """Video Data Class: Represents a video as posted on The Blue Alliance."""

    @property
    def key(self):
        """The key of the represented video."""
        return self['key']

    @property
    def type(self):
        """The type of represented video."""
        return self['type']

    # When referenced in terminal without called attribute, output video information.
    def __repr__(self):
        """Return video information when referenced."""
        return '<tbapi.Video: Video for {}>'.format(self['match'])


# AllianceSet Data Class:  Wrapper for both Alliances that competed in a given Match.
class AllianceSet(Data):
    """AllianceSet Data Class:  Wrapper for both :class:`Alliance` objects that competed in a given match."""

    @property
    def red(self):
        """:class:`Alliance`: The red Alliance for a given Match.

            Alias: *r*"""
        return Alliance(self['red'], self.parser, self.options)

    @property
    def r(self):
        return Alliance(self['red'], self.parser, self.options)

    @property
    def blue(self):
        """:class:`Alliance`: The blue Alliance for a given Match.

            Alias: *b*"""
        return Alliance(self['blue'], self.parser, self.options)

    @property
    def b(self):
        return Alliance(self['blue'], self.parser, self.options)

    # When referenced in terminal without called attribute, output alliance set information.
    def __repr__(self):
        """Return set information when referenced."""
        red_alliance = ''
        blue_alliance = ''

        for key in self['red']['team_keys']:
            red_alliance += key[3:] + ', '

        for key in self['blue']['team_keys']:
            blue_alliance += key[3:] + ', '

        return '<tbapi.AllianceSet: RED[{}], BLUE[{}]>'.format(red_alliance[:-2], blue_alliance[:-2])


# Alliance Data Class:  Represents an Alliance that participated in a given Match.
class Alliance(Data):
    """Alliance Data Class:  Represents an Alliance that participated in a given Match."""

    @property
    def score(self):
        """The score earned by the represented Alliance in a given Match."""
        return self['score']

    @property
    def team_keys(self):
        """A list of team keys representing the teams that participated on the represented Alliance."""
        return self['team_keys']

    @property
    def teams(self):
        """:class:`DataList`: A list of :class:`Team` objects that participated on the represented Alliance."""
        team_list = DataList([], [])

        for team_key_item in self['team_keys']:
            team_obj = self.parser.get_team(team_key_item, force_new=self.options['force_new'], force_cache=self.options['force_cache'], log_cache=self.options['log_cache'])

            team_list.append(team_obj)
            team_list.raw.append(dict(team_obj))

        return team_list

    @property
    def surrogate_team_keys(self):
        """A list of team keys representing teams that acted as surrogates on the represented Allliance."""
        return self['surrogate_team_keys']

    @property
    def surrogate_teams(self):
        """:class:`DataList`: A list of :class:`Team` objects that acted as surrogates on the represented Allliance.

            Alias: *surrogates*"""
        surrogate_team_list = DataList([], [])

        for team_key_item in self['surrogate_team_keys']:
            team_obj = self.parser.get_team(team_key_item, force_new=self.options['force_new'], force_cache=self.options['force_cache'], log_cache=self.options['log_cache'])

            surrogate_team_list.append(team_obj)
            surrogate_team_list.raw.append(dict(team_obj))

        return surrogate_team_list

    @property
    def surrogates(self):
        surrogate_team_list = DataList([], [])

        for team_key_item in self['surrogate_team_keys']:
            team_obj = self.parser.get_team(team_key_item, force_new=self.options['force_new'], force_cache=self.options['force_cache'], log_cache=self.options['log_cache'])

            surrogate_team_list.append(team_obj)
            surrogate_team_list.raw.append(dict(team_obj))

        return surrogate_team_list

    # When referenced in terminal without called attribute, output alliance information.
    def __repr__(self):
        """Return alliance information when referenced."""
        alliance_members = ''

        for key in self['team_keys']:
            alliance_members += key[3:] + ' '

        return '<tbapi.Alliance: {}>'.format(alliance_members[:-1])


# TeamAlliance Data Class: Represents a Team's Association to a given Alliance.
class TeamAlliance(Data):
    """TeamAlliance Class:  Represents a Team's Association to a given Alliance."""

    @property
    def backup(self):
        """:class:`Backup`: Information on Backup Swaps involving the associated team."""
        if self['backup'] != None:
            return Backup(self['backup'], self.parser, self.options)
        else:
            return None

    @property
    def name(self):
        """The name of the given Alliance."""
        return self['name']

    @property
    def number(self):
        """The number of the given Alliance."""
        return self['number']

    @property
    def pick(self):
        """The pick number of the given Alliance."""
        return self['pick']

    @property
    def pick_position(self):
        """The pick number of the given Alliance."""
        return self['pick']

    # When referenced in terminal without called attribute, output customized string.
    def __repr__(self):
        """Return custom string when referenced."""
        return '<tbapi.TeamAlliance>'

    # When converted to a string, return the alliance number.
    def __str__(self):
        """Return the Robot Key when converted to a String."""
        return self['name']

    # When converted to an integer, return the alliance number.
    def __int__(self):
        """Return the robot build year when converted to an Integer."""
        return int(self['number']) # Convert to an integer, in case of errors in JSON parsing.


# Backup Data Class: Information on Backup Swaps involving a given Team on a given Alliance at a given Event.
class Backup(Data):
    """Backup Data Class: Information on Backup Swaps involving a given Team on a given Alliance at a given Event."""

    @property
    def team_in(self):
        """The Team that joined the Alliance."""
        return self['in']

    @property
    def team_out(self):
        """The Team that left the Alliance (in terms of playing)."""
        return self['out']

    # When referenced in terminal without called attribute, output customized string.
    def __repr__(self):
        """Return custom string when referenced."""
        return '<tbapi.Backup>'


# Breakdown Data Class: Fluid Match Statistics for a given Alliance in a given Match.
class Breakdown(Data):
    """Breakdown Class: Provides access to Fluid Match Statistics for a given Alliance in a given Match.

        Each FIRST Robotics Competition Game gathers different statistics that are related to it's gameplay.  This class provides access to these \"Fluid\" keys for use in your software."""

    # Get a fluid key from the internal data dictionary.
    def get(self, key):
        """Get the statistic associated with a provided fluid key from the internal data dictionary based on it's reference name.  

            Raises a :class:`FluidKeyError` if the fluid key is not available in this :class:`Breakdown` object."""
        if not key in self.keys():
            raise FluidKeyError
        else:
            return self[key]

    # Get a list of included fluid keys
    @property
    def list(self):
        """A list of fluid keys that are represented by this :class:`Breakdown` object."""
        return list(self.keys())

    # When referenced in terminal without called attribute, output customized string.
    def __repr__(self):
        """Return custom string when referenced."""
        return '<tbapi.Breakdown>'

# BreakdownSet Data Class: Wrapper for Breakdowns for a given Match.
class BreakdownSet(Data):
    """BreakdownSet Data Class: Wrapper for Breakdowns for a given Match."""

    @property
    def red(self):
        """Breakdown for the red Alliance for a given Match.

            Alias: *r*"""
        return Breakdown(self['red'], self.parser, self.options)

    @property
    def r(self):
        return Breakdown(self['red'], self.parser, self.options)

    @property
    def blue(self):
        """Breakdown for the blue Alliance for a given Match.

            Alias: *b*"""
        return Breakdown(self['blue'], self.parser, self.options)

    @property
    def b(self):
        return Breakdown(self['blue'], self.parser, self.options)

    # When referenced in terminal without called attribute, output breakdown set information.
    def __repr__(self):
        """Return breakdown set information when referenced."""
        return '<tbapi.BreakdownSet>'


# Match Data Class: Represents a match played at a given event and its corresponding data.
class Match(Data):
    """Match Data Class: Represents a match at a given event and its corresponding data."""

    @property
    def key(self):
        """The Match Key for the given match.  Includes event_key as a Substring."""
        return self['key']

    @property
    def event_key(self):
        """The Event Key of the Event at which the given match was played."""
        return self['event_key']

    @property
    def comp_level(self):
        """The Competition Level at which the given Match was played. (qm, qf, sf, f, etc.)"""
        return self['comp_level']

    @property
    def level(self):
        """The Competition Level at which the given Match was played. (qm, qf, sf, f, etc.)"""
        return self['comp_level']

    @property
    def match_number(self):
        """The ID number of the given Match"""
        return self['match_number']

    @property
    def number(self):
        """The ID number of the given Match"""
        return self['match_number']

    @property
    def set_number(self):
        """The ID number of the given Match in the current Match set."""
        return self['set_number']

    @property
    def raw_time(self):
        """A Unix-Time representation of the Match Time."""
        return self['time']

    @property
    def time(self):
        """A Datetime representation of the Match Time."""
        return datetime.datetime.fromtimestamp(int(self['time']))

    @property
    def raw_predicted_time(self):
        """A Unix-Time representation of the Scheduled Match Time."""
        return self['predicted_time']

    @property
    def predicted_time(self):
        """A Datetime representation of the Scheduled Match Time."""
        return datetime.datetime.fromtimestamp(int(self['predicted_time']))

    @property
    def raw_post_time(self):
        """A Unix-Time representation of the Score Post Time."""
        return self['post_result_time']

    @property
    def raw_post_result_time(self):
        """A Unix-Time representation of the Score Post Time."""
        return self['post_result_time']

    @property
    def post_time(self):
        """A Datetime representation of the Score Post Time."""
        return datetime.datetime.fromtimestamp(int(self['post_result_time']))

    @property
    def post_result_time(self):
        """A Datetime representation of the Score Post Time."""
        return datetime.datetime.fromtimestamp(int(self['post_result_time']))

    @property
    def videos(self):
        """A DataList of Videos showing the given Match."""
        modified_video_list = []

        for video_item in self['videos']:
            modified_video = video_item.copy()
            modified_video['match'] = self['key']
            modified_video_list += [modified_video]

        return DataList([Video(video_item, self.parser, self.options) for video_item in modified_video_list], self['videos'])

    @property
    def winning_alliance(self):
        """A String representing the color of the winning alliance."""
        return self['winning_alliance']

    @property
    def alliances(self):
        """A Wrapper containing both alliances that participated in the represented match."""
        return AllianceSet(self['alliances'], self.parser, self.options)

    @property
    def red_alliance(self):
        """The red Alliance that participated in the represented match."""
        return Alliance(self['alliances']['red'], self.parser, self.options)

    @property
    def blue_alliance(self):
        """The red Alliance that participated in the represented match."""
        return Alliance(self['alliances']['blue'], self.parser, self.options)

    @property
    def teams(self):
        """:class:`DataList`: A list of :class:`Team` objects that participated in the represented match, independant of alliance."""
        team_keys = self['alliances']['blue']['team_keys'] + self['alliances']['red']['team_keys']
        team_list = DataList([],[])

        for team_key_item in team_keys:
            team_obj = self.parser.get_team(team_key_item, force_new=self.options['force_new'], force_cache=self.options['force_cache'], log_cache=self.options['log_cache'])

            team_list.append(team_obj)
            team_list.raw.append(dict(team_obj))

        return team_list

    @property
    def score_breakdown(self):
        """:class:`BreakdownSet`: Fluid Statistics regarding the represented match.

            Alias: *breakdown*"""
        return BreakdownSet(self['score_breakdown'], self.parser, self.options)

    @property
    def breakdown(self):
        return BreakdownSet(self['score_breakdown'], self.parser, self.options)

    # When referenced in terminal without called attribute, output match information.
    def __repr__(self):
        """Return match information when referenced."""
        return '<tbapi.Match: {} - {}>'.format(self['key'], '{} Alliance ({} pts)'.format(self['winning_alliance'].capitalize(), self['alliances'][self['winning_alliance']]['score']) if not self['winning_alliance'] == '' else 'tied')


# Awards Data Class: Represents an Award given at a defined Event.
class Award(Data):
    """Awards Data Class: Represents an Award given at a defined Event."""

    @property
    def name(self):
        """The name of the represented Award."""
        return self['name']

    @property
    def award_type(self):
        """An Integer representing the type of represented Award."""
        return self['award_type']

    @property
    def type(self):
        """An Integer representing the type of represented Award."""
        return self['award_type']

    @property
    def event_key(self):
        """The key for the Event at which the Award was given."""
        return self['event_key']
    
    @property
    def event(self):
        """:class:`Event`: The Event at which the Award was given."""
        return self.parser.get_event(self['event_key'], force_new=self.options['force_new'], force_cache=self.options['force_cache'], log_cache=self.options['log_cache'])

    @property
    def recipient_list(self):
        """A list of Recipients to which the represented award was presented."""
        return DataList([Recipient(recipient_item) for recipient_item in self['recipient_list']], self['recipient_list'])

    # When referenced in terminal without called attribute, output award information.
    def __repr__(self):
        """Return Award Information when referenced."""
        return '<tbapi.Award: {} @ {}'.format(self['name'], self['event_key'])


# Recipient Data Class: Represents the Recipient of an Award given at a defined Event.
class Recipient(Data):
    """Recipient Data Class: Represents the Recipient of an Award given at a defined Event."""

    @property
    def team_key(self):
        """The key of the Recipient Team"""
        return self['team_key']

    @property
    def team(self):
        """:class:`Team`: The Recipient Team"""
        return self.parser.get_team(self['team_key'], force_new=self.options['force_new'], force_cache=self.options['force_cache'], log_cache=self.options['log_cache'])

    @property
    def awardee(self):
        """The Individual Person to who'm the award was presented."""
        return self['awardee']
    
    # When referenced in terminal without called attribute, output recipient information.
    def __repr__(self):
        """Return Recipient Information when referenced."""
        return '<tbapi.Recipient: {}'.format(self['team_key'])


# Cache Database Defaults Class: Used for setting up default columns in the cache database.
class CacheTable(object):
    """Database Cache Defaults:  Holds default cache table column information."""
    def __init__(self):
        self.columns = ['REQUEST', 'RESPONSE', 'REQUESTED', 'LAST_MODIFIED', 'MAX_AGE']
        self.datatypes = ['TEXT PRIMARY KEY NOT NULL', 'TEXT NOT NULL', 'TEXT NOT NULL', 'TEXT NOT NULL', 'TEXT NOT NULL']
        self.seed = []


# Main Parser Class:  All requests routed through this class's methods.
class Parser:
    """TBA Parser Class: Routes API requests and handles caching. Requires v3 API Key from TBA.

    :param str api_key: API Key used for connection to The Blue Alliance API Servers.  Get an API Key from your `TBA Account Settings <tba_account_settings_>`_.
    :param bool cache: *(opt)* Enabling of the In-Built Caching System. *(default: True)*
    :param bool local: *(opt)* Store cache Database in the local directory rather than globally in the python directory. *(default: False)*
    :param bool force_cache: *(opt)* Force the :class:`Parser` to pull data for the In-Built Cache before attempting TBA Connection. *(default: False)*
    :param bool log_cache: *(opt)* Log Caching Information to the Terminal while attempting to interact with the In-Built Cache. *(default: False)*
    :param int cache_multiplier: *(opt)* Multiplier for die-times of cache data. Allows data to be used by the standard caching methods after their standard accuracy period. *(default: 1)*
    
    All Parser Class Methods have the following optional arguments:

    :param bool force_new: *(opt)* Force a new request from The Blue Alliance servers, ignoring the cache response or 304 Response Headers. *(default: False)*
    :param bool force_cache: *(opt)* Force a call to the cache, regardless of global cache settings. *(default: False)*
    :param bool log_cache: *(opt)* Log Caching Information to the Terminal while attempting to interact with the In-Built Cache. *(default: False)*"""

    # Initiate Information needed for connection to TBA v3 (api_key)
    def __init__(self, api_key, *, cache=True, local=False, force_cache=False, log_cache=False, cache_multiplier=1):
        self.api_key = api_key # TBA API v3 API key
        self.cache = cache
        self.force_cache = force_cache
        self.log_cache = log_cache
        self.cache_multiplier = cache_multiplier
        self.base_url = 'http://www.thebluealliance.com/api/v3'

        if self.cache:
            if local is False:
                self.storage_path = os.path.dirname(sys.executable) + '/.tbapi'

                if not os.path.exists(self.storage_path):
                    try:
                        os.makedirs(self.storage_path)
                    except:
                        self.storage_path = os.getcwd()

                self.cache_db = sq.Connect(self.storage_path + '/cache')
            else:
                self.cache_db = sq.Connect('tbapi-cache')


            if not self.cache_db.table('cache_data').tableExists():
                cache_preset = CacheTable()
                self.cache_db.table('cache_data').init(cache_preset)

    # Modify the response when outputted in the terminal or when converted to a string.
    def __repr__(self):
        """Modified Response Return"""
        return '<tbapi.Parser: \'{}\'>'.format(self.api_key)

    # Method to pull JSON array from TBA v3 API.  Includes Caching and Offline Support.
    def pull_response_json(self, path, *, force_new=False, force_cache=False, log_cache=False):
        """Pull the JSON response to a given path from the TBA API servers or the response cache.
        
        :param string path: The URL to pull data from, without the base string 'http://www.thebluealliance.com/api/v3'."""
        
        if not path.startswith('/'):
            path = '/' + path

        current_time = datetime.datetime.now() # Get the Current Time at the start of method execution

        if (self.cache or force_cache) and force_new == False: # If caching is enabled, and a new response is not forced, attempt pulling from cache

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
                    cache_expire_offset = float(cache_max_age) * float(self.cache_multiplier)
                    cache_expire = cache_requested + datetime.timedelta(seconds=int(cache_expire_offset))

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
    # Get TBA API Status
    def get_status(self, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`Status`: the Status of The Blue Alliance's API and its Apps."""
        return Status(self.pull_response_json('/status', force_new=False, force_cache=False, log_cache=False), self)

    # Get a List of FRC Teams
    def get_team_list(self, *, page=None, year=None, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`Team` objects.
        
        :param int page: *(opt)* The page of teams to fetch.  Argument must be named explicitly when passing.  If not included, method will pull all available pages.
        :param int year: *(opt)* The year to fetch competing teams for. Argument must be named explicitly when passing.  If not included, method will pull all teams that have ever competed and are recorded in the TBA databases."""
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
                team_list.json_array += partial_list.json_array

        return team_list

    # HELPER: get single page of team data
    def __get_team_list_page(self, page, *, year=None, force_new=False, force_cache=False, log_cache=False):
        """HELPER METHOD: Get a single page of teams."""
        return_array = self.pull_response_json('/teams/{}{}'.format('{}/'.format(year) if not year is None else '', str(page)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)

        page_list = DataList([], return_array)

        for item in return_array:
            page_list.append(Team(item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}))

        return page_list

    # Get a List of FRC Team Keys
    def get_team_key_list(self, *, page=None, year=None, force_new=False, force_cache=False, log_cache=False):
        """Get a list of team keys.

        :param int page: *(opt)* The page of teams to fetch.  Argument must be named explicitly when passing.  If not included, method will pull all available pages.
        :param int year: *(opt)* The year to fetch competing teams for. Argument must be named explicitly when passing.  If not included, method will pull all teams that have ever competed and are recorded in the TBA databases."""
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
        """:class:`Team`: Get a single team.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`."""
        return Team(self.pull_response_json('/team/{}'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache), self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache})

    # Get a list containing the years in which a given team has participated
    def get_team_years_participated(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`list`: Get a list containing the years in which a given team has participated.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`."""
        return self.pull_response_json('/team/{}/years_participated'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
    
    # Get a list of Districts that the given team has competed in
    def get_team_districts(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`District` objects in which the given team has competed in.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`."""
        district_list = self.pull_response_json('/team/{}/districts'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([District(district_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for district_item in district_list], district_list)

    # Get a list of Robots built and operated by a given team
    def get_team_robots(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`Robot` objects built and operated by a given team.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`."""
        robot_list = self.pull_response_json('/team/{}/robots'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Robot(robot_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for robot_item in robot_list], robot_list)

    # Get a list of Social Media Presences operated by a given team.
    def get_team_social_media(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`Media` objects (Social Media Prescenses) operated by a given team.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`.
            
        Alias: *get_team_social*"""
        social_list = self.pull_response_json('/team/{}/social_media'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Media(social_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for social_item in social_list], social_list)

    # ALIAS: get_team_social_media
    def get_team_social(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        return self.get_team_social_media(team_identifier, force_new=force_new, force_cache=force_cache, log_cache=log_cache)

    # Get a list of events attended by a given team
    def get_team_events(self, team_identifier, year=None, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`Event` objects attended by a given team.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`.
        :arg int year: *(opt)* The Year to pull events for.  If not included, method will pull all events in which a team has competed in."""
        if not year:
            event_list = self.pull_response_json('/team/{}/events'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
            return DataList([Event(event_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for event_item in event_list], event_list)
        else:
            event_list = self.pull_response_json('/team/{}/events/{}'.format(self.__get_team_key(team_identifier), str(year)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
            return DataList([Event(event_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for event_item in event_list], event_list)

    # Get a list of Matches played by a given Team at a given Event
    def get_team_event_matches(self, team_identifier, event_key, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`Match` objects played by a given Team at a given Event.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`.
        :arg str event_key: The :attr:`event_key` of the desired Event, following the format `YYYY[EVENT_CODE]`, where `YYYY` is the the year and `EVENT_CODE` is the `event code <https://docs.google.com/spreadsheet/ccc?key=0ApRO2Yzh2z01dExFZEdieV9WdTJsZ25HSWI3VUxsWGc>`_ of the event."""
        match_list = self.pull_response_json('/team/{}/event/{}/matches'.format(self.__get_team_key(team_identifier), event_key), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Match(match_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for match_item in match_list], match_list)

    # Get a list of Awards presented to a given Team at a given Event
    def get_team_event_awards(self, team_identifier, event_key, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`Award` objects presented to a given Team at a given Event.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`.
        :arg str event_key: The :attr:`event_key` of the desired Event, following the format `YYYY[EVENT_CODE]`, where `YYYY` is the the year and `EVENT_CODE` is the `event code <https://docs.google.com/spreadsheet/ccc?key=0ApRO2Yzh2z01dExFZEdieV9WdTJsZ25HSWI3VUxsWGc>`_ of the event."""
        award_list = self.pull_response_json('/team/{}/event/{}/awards'.format(self.__get_team_key(team_identifier), event_key), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Award(award_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for award_item in award_list], award_list)

    # Get information about the status of a given team at a given event
    def get_team_event_status(self, team_identifier, event_key, *, force_new=False, force_cache=False, log_cache=False):
        """Get information about the status of a given team at a given event.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`.
        :arg str event_key: The :attr:`event_key` of the desired Event, following the format `YYYY[EVENT_CODE]`, where `YYYY` is the the year and `EVENT_CODE` is the `event code <https://docs.google.com/spreadsheet/ccc?key=0ApRO2Yzh2z01dExFZEdieV9WdTJsZ25HSWI3VUxsWGc>`_ of the event."""
        return self.pull_response_json('/team/{}/event/{}/status'.format(self.__get_team_key(team_identifier), event_key), force_new=force_new, force_cache=force_cache, log_cache=log_cache)

    # Get a list of Awards presented to a given Team throughout their History
    def get_team_awards(self, team_identifier, year=None, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`Award` objects presented to a given Team throughout their History.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`.
        :arg int year: *(opt)* The Year to pull awards for.  If not included, method will pull all awards won by the team."""
        award_list = self.pull_response_json('/team/{}/awards{}'.format(self.__get_team_key(team_identifier), '/{}'.format(year) if year else ''), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Award(award_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for award_item in award_list], award_list)

    # Get a list of Matches played by a given Team throughout their History
    def get_team_matches(self, team_identifier, year=None, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`Match` objects played by a given Team throughout their History.
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`.
        :arg int year: *(opt)* The Year to pull matches for.  If not included, method will pull all matches played by the team."""
        if year:
            return self.__get_team_year_matches(team_identifier, year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        else:
            try:
                rookie_year = int(self.get_team(team_identifier, force_cache=True, log_cache=log_cache).rookie_year)
            except:
                raise Exception('YearParseError:  Could not find team\'s rookie year.')

            try:
                current_year = int(self.get_status(force_new=force_new, force_cache=force_cache, log_cache=log_cache).current_season)
            except:
                raise Exception('YearParseError:  Could not find current FRC Season.')

            final_data = DataList([], [])

            for test_year in range(rookie_year, current_year + 1):
                try:
                    partial_data = self.__get_team_year_matches(team_identifier, test_year)

                    final_data += partial_data
                    final_data.json_array += partial_data.json_array
                except EmptyError:
                    pass

            return final_data

    # HELPER: Get a single page of Team Matches from a given year
    def __get_team_year_matches(self, team_identifier, year, *, force_new=False, force_cache=False, log_cache=False):
        """HELPER: Get a single page of Team Matches from a given year."""
        match_list = self.pull_response_json('/team/{}/matches/{}'.format(self.__get_team_key(team_identifier), str(year)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Match(match_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for match_item in match_list], match_list)

    # Get a list of Media provided by a given Team throughout their History
    def get_team_media(self, team_identifier, year=None, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: a list of :class:`Media` objects provided by a given Team throughout their History
        
        :arg int/str team_identifier: Either a team's :attr:`team_key` or their :attr:`team_number`.
        :arg int year: *(opt)* The Year to pull media for.  If not included, method will pull all media provided by the team."""
        if year:
            return self.__get_team_year_media(team_identifier, year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        else:
            try:
                rookie_year = int(self.get_team(team_identifier, force_cache=True, log_cache=log_cache).rookie_year)
            except:
                raise Exception('YearParseError:  Could not find team\'s rookie year.')

            try:
                current_year = int(self.get_status(force_new=force_new, force_cache=force_cache, log_cache=log_cache).current_season)
            except:
                raise Exception('YearParseError:  Could not find current FRC Season.')

            final_data = DataList([], [])

            for test_year in range(rookie_year, current_year + 1):
                try:
                    partial_data = self.__get_team_year_media(team_identifier, test_year)

                    final_data += partial_data
                    final_data.json_array += partial_data.json_array
                except EmptyError:
                    pass

            return final_data

    # HELPER: Get a single page of Team Media from a given year
    def __get_team_year_media(self, team_identifier, year, *, force_new=False, force_cache=False, log_cache=False):
        """HELPER: Get a single page of Team Media from a given year."""
        media_list = self.pull_response_json('/team/{}/media/{}'.format(self.__get_team_key(team_identifier), str(year)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Media(media_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for media_item in media_list], media_list)

    # Get a list of Events that took place in a given year or throughout FIRST history
    def get_event_list(self, year=None, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`DataList`: Get a list of :class:`Event` objects.
        
        :arg int year: The year to grab events for."""
        if year:
            return self.__get_event_list_year(year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        else:
            try:
                current_year = int(self.get_status(force_new=force_new, force_cache=force_cache, log_cache=log_cache).current_season)
            except:
                raise Exception('YearParseError:  Could not find current FRC Season.')

            final_data = DataList([], [])

            for test_year in range(1992, current_year + 1):
                try:
                    print(test_year)
                    partial_data = self.__get_event_list_year(test_year)

                    final_data += partial_data
                    final_data.json_array += partial_data.json_array
                except EmptyError:
                    pass

            return final_data

    
    # HELPER: Get a single page of Events from a given year
    def __get_event_list_year(self, year, *, force_new=False, force_cache=False, log_cache=False):
        """HELPER: Get a single page of Events from a given year."""
        event_list = self.pull_response_json('/events/{}'.format(str(year)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Event(event_item, self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache}) for event_item in event_list], event_list)

    # Get a single event, by event key.
    def get_event(self, event_key, *, force_new=False, force_cache=False, log_cache=False):
        """:class:`Event`: Get a single event by it's event_key.
        
        :arg str event_key: The :attr:`event_key` of the desired Event, following the format `YYYY[EVENT_CODE]`, where `YYYY` is the the year and `EVENT_CODE` is the `event code <https://docs.google.com/spreadsheet/ccc?key=0ApRO2Yzh2z01dExFZEdieV9WdTJsZ25HSWI3VUxsWGc>`_ of the event."""
        return Event(self.pull_response_json('/event/{}'.format(event_key), force_new=force_new, force_cache=force_cache, log_cache=log_cache), self, {'force_new':force_new, 'force_cache':force_cache, 'log_cache':log_cache})