"""TBApi - Python Library for The Blue Alliance API v3"""

import os
import sys
import json
import datetime
import requests
from SQLiteHelper import SQLiteHelper as sq # SQLite3 Wrapper for easier reading and programming
import numpy as np
from numpy import array as np_array


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

    def filter(self, attr_name, attr_value):
        """Filter the stored objects by a given attribute.  Returns a new DataList."""

        return_list = self.__class__([], {})

        for data_object in self:
            desired_attribute = getattr(data_object, str(attr_name), None)

            if desired_attribute == attr_value:
                return_list.append(data_object)
                return_list.raw.append(data_object.raw)

        return return_list


# Basic Data Class:  Stores information about data returned by TBA
class Data(object):
    def __init__(self, json_array):
        self.raw = json_array

        self.is_error = False

        if 'error' in json_array:
            if json_array['error'] is True:
                self.is_error = True


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
    def __init__(self, api_key, cache=True, force_cache=False, log_cache=False):
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
    def pull_response_json(self, path, force_new=False, force_cache=False, log_cache=False):
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
                header = {'X-TBA-Auth-Key': self.api_key, 'If-Modified-Since': cache_last_modified_str} # Form headers, but substitute in last_modified string from database to see if data has changed since last database pull

                if force_cache or self.force_cache:
                    if self.log_cache or log_cache:
                        print('Forcing Read from Cache...')

                    return cache_response

                try:
                    response = requests.get(request, headers=header)
                except:
                    cache_expire = cache_requested + datetime.timedelta(seconds=int(cache_max_age))

                    if current_time <= cache_expire:
                        if self.log_cache or log_cache:
                            print('Offline: Reading from Cache...')

                        return cache_response
                    else:
                        if self.log_cache or log_cache:
                            print('Offline: No Cache Available...')

                        return {'error': True}

                if response.status_code == 304:
                    if self.log_cache or log_cache:
                        print('304 NOT MODIFIED: Reading from Cache...')

                    return cache_response
                else:
                    if self.log_cache or log_cache:
                        print('Data Modified, Ignoring Cache...')

                    json_array = response.json()

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

                    return json_array

        request = (self.base_url + path)
        header = {'X-TBA-Auth-Key': self.api_key}

        try:
            response = requests.get(request, headers=header)

            if self.log_cache or log_cache:
                print('No Cache Available, Pulling New Data...')
        except:
            if self.log_cache or log_cache:
                print('Offline: No Cache Available...')

            return {'error': True}

        json_array = response.json()

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

        return json_array





