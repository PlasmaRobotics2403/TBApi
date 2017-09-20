"""TBApi v3 Models"""

from .exceptions import InvalidKeyError


class DataList(list):
    """Extension of :class:`list` used for storing data returns with multiple objects
    
    `raw` Attribute contains the raw JSON through which the internal objects were created"""
    def __init__(self, *, valid=True, objects=[], raw=[]):
        super().__init__()

        self.valid = valid

        if valid:
            self.extend(objects)
            self.raw = raw

    def filter(self, **attrs):
        """Find all internal elements that match a set of specified attributes
        
        Returns a new DataList containing matching elements"""

        def predicate(element):
            for attr, val in attrs.items():
                nested = attr.split('__')
                obj = element

                for attribute in nested:
                    obj = getattr(obj, attribute)

                if obj != val:
                    return False
            return True
            
        match_return = DataList()

        matches = filter(predicate, self)

        match_return.extend(list(matches))
        match_return.raw.extend([list(element) for element in match_return])
        
        return match_return

    def __repr__(self):
        return '<tbapi.DataList {}>'.format(super().__repr__())


class Data(object):
    """Basic Data Class, extended for other Data Modules.  Data Classes should have no never need to be created by the end user.

    .. warning::
        Modifcations to the internal dictionary structure of a :class:`Data` or derived object will be reflected in returned values.  Modify at your own risk, as this may cause incompatibilities within the library."""

    ALIAS = {}
    PREDICATES = {}

    def __init__(self, raw):
        if isinstance(raw, dict):
            self.__raw = raw
        if isinstance(raw, list):
            self.__raw = dict(enumerate(raw))
        else:
            try:
                raw_dict = dict(raw)
            except:
                self.__raw = {}
            else:
                self.__raw = raw_dict

    def flatten(self):
        """Flatten the :class:`Data` to a raw dictionary"""
        return self.__raw

    def __get_data_value(self, name):
        if name in self.ALIAS:
            key = self.ALIAS[name]
        else:
            key = name

        if name in self.PREDICATES:
            predicate = self.PREDICATES[name]
        elif key in self.PREDICATES:
            predicate = self.PREDICATES[key]
        else:
            predicate = None

        if key in self.__raw:
            value = self.__raw[key]

            if predicate:
                value = predicate(value)

            return value
        else:
            raise InvalidKeyError

    def __set_data_value(self, name, value):
        if name in self.ALIAS:
            name = self.ALIAS[name]

        self.__raw[name] = value

    def __getattr__(self, attribute):
        return self.__get_data_value(attribute)

    def __setattr__(self, attribute, value):
        if attribute.startswith('_'):
            object.__setattr__(self, attribute, value)
        else:
            self.__set_data_value(attribute, value)

    def __getitem__(self, key):
        if key.startswith('_'):
            return getattr(self, key)
        else:
            return self.__get_data_value(key)

    def __setitem__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            self.__set_data_value(key, value)

    def __repr__(self):
        return '<tbapi.Data>'


class API_Status_App_Version(Data):
    """The Current Status of an App on a Specific App Platform

    ATTRIBUTE ALIASES:
    `min_app_version` > `min`, `minimum`
    `latest_app_version` > `max`, `maximum`, `latest`"""

    ALIAS = {
        'min': 'min_app_version',
        'minimum': 'min_app_version',
        'max': 'latest_app_version',
        'maximum': 'latest_app_version',
        'latest': 'latest_app_version'
    }

    def __repr__(self):
        return '<tbapi.API_Status_App_Version: min_app_version={}, latest_app_version={}>'.format(self.min_app_version, self.latest_app_version)


class API_Status(Data):
    """The Current Status of The Blue Alliance API v3"""

    PREDICATES = {
        'ios': API_Status_App_Version,
        'android': API_Status_App_Version
    }

    def __repr__(self):
        return '<tbapi.API_Status: is_datafeed_down={}>'.format(self.is_datafeed_down)


class Team(Data):
    """A Representation of a specific FRC Team

    ATTRIBUTE ALIASES:
    `nickname` > `nick`
    'team_number' > 'number'
    `state_prov` > `state`, `province`
    `postal_code` > `zip`, `zip_code`"""

    ALIAS = {
        'nick': 'nickname',
        'number': 'team_number',
        'state': 'state_prov',
        'provice': 'state_prov',
        'zip': 'postal_code',
        'zip_code': 'postal_code'
    }

    def __repr__(self):
        return '<tbapi.Team: Team {} - {}>'.format(self.team_number, self.nickname)


class Team_Simple(Team):
    """A Concise Representation of a specific FRC Team

    ATTRIBUTE ALIASES:
    `nickname` > `nick`
    'team_number' > 'number'
    `state_prov` > `state`, `province`"""

    ALIAS = {
        'nick': 'nickname',
        'number': 'team_number',
        'state': 'state_prov',
        'provice': 'state_prov'
    }

    def __repr__(self):
        return '<tbapi.Team_Simple: Team {} - {}>'.format(self.team_number, self.nickname)


class Team_Robot(Data):
    """A Representation of a Robot belonging to a specific FRC Team

    ADDITIONAL ATTRIBUTES:
    `number`, `team_number` = Team Number of the Owning Team

    ATTRIBUTE ALIASES:
    `robot_name` > `name`"""

    ALIAS = {
        'name': 'robot_name',
        'number': 'team_key',
        'team_number': 'team_key'
    }

    def __number_predicate(self, team_key):
        return int(team_key[3:])

    PREDICATES = {
        'team_number': __number_predicate,
        'number': __number_predicate
    }

    def __repr__(self):
        return '<tbapi.Team_Robot: {} by Team {}>'.format(self.robot_name, self.team_key[3:])


class District_List(Data):
    """Information Regarding a Specific District during a Specific Year
    
    ATTRIBUTE ALIASES:
    `display_name` > `long_name`, `name`"""

    ALIAS = {
        'long_name': 'display_name',
        'name': 'display_name'
    }

    def __repr__(self):
        return '<tbapi.District_List: {}>'.format(self.display_name)


class Webcast(Data):
    """A Representation of a Webcast at an FRC Event"""

    def __repr__(self):
        return '<tbapi.Webcast: type={}>'.format(self.type)


class Event(Data):
    """A Representation of a specific FRC Event
    
    ATTRIBUTE ALLIASES:
    `event_code` > `code`
    `event_type` > `type`
    `state_prov` > `state`, `province`
    `start_date` > `start`
    `end_date` > `end`
    `postal_code` > `zip`, `zip_code`"""

    ALIAS = {
        'code': 'event_code',
        'type': 'event_type',
        'state': 'state_prov',
        'province': 'state_prov',
        'start': 'start_date',
        'end': 'end_date',
        'zip': 'postal_code',
        'zip_code': 'postal_code'
    }

    def __webcast_list_predicate(self, raw):
        webcast_list = [Webcast(raw_value) for raw_value in raw]
        webcast_return = DataList(objects=webcast_list, raw=[webcast.flatten() for webcast in webcast_list])
        return webcast_return

    PREDICATES = {
        'district': District_List,
        'webcasts': __webcast_list_predicate
    }

    def __repr__(self):
        return '<tbapi.Event: {}>'.format(self.name)


class Event_Simple(Event):
    """A Simplified Representation of a specific FRC Event
    
    ATTRIBUTE ALLIASES:
    `event_code` > `code`
    `event_type` > `type`
    `state_prov` > `state`, `province`
    `start_date` > `start`
    `end_date` > `end`"""

    ALIAS = {
        'code': 'event_code',
        'type': 'event_type',
        'state': 'state_prov',
        'province': 'state_prov',
        'start': 'start_date',
        'end': 'end_date',
    }

    PREDICATES = {
        'district': District_List
    }

    def __repr__(self):
        return '<tbapi.Event_Simple: {}>'.format(self.name)
    

class WLT_Record(Data):
    """A Win-Loss-Tie Record for a Team or Alliance
    
    ATTRIBUTE ALLIASES:
    `wins` > `w`, `win`
    `losses` > `l`, `loss`
    `ties` > `t`, `tie`"""

    ALIAS = {
        'w': 'wins',
        'win': 'wins',
        'l': 'losses',
        'loss': 'losses',
        't': 'ties',
        'tie': 'ties'
    }

    def __repr__(self):
        return '<tbapi.WLT_Record>'


class Team_Ranking(Data):
    """Ranking Data corresponding to a given Team during Qualifications at a given Event

    ADDITIONAL ATTRIBUTES:
    `number`, `team_number` = Team Number of the Corresponding Team
    
    ATTRIBUTE ALLIASES:
    `dq` > `disqualified`
    `team_key` > `key`
    `qual_average` > `average`
    `record` > `wlt`"""

    ALIAS = {
        'disqualified': 'dq',
        'average': 'qual_average',
        'key': 'team_key',
        'wlt': 'record',
        'number': 'team_key',
        'team_number': 'team_key'
    }

    def __number_predicate(self, team_key):
        return int(team_key[3:])

    PREDICATES = {
        'team_number': __number_predicate,
        'number': __number_predicate,
        'record': WLT_Record,
    }

    def __repr__(self):
        return '<tbapi.Team_Ranking: Team {}>'.format(self.team_key[3:])


class Rank_Sort_Info(Data):
    """Information Regarding a Sort Category used within Qualifications at a given Event"""

    def __repr__(self):
        return '<tbapi.Rank_Sort_Info: {} ({}p)>'.format(self.name, self.precision)


class Team_Event_Status_rank(Data):
    """A Specific Team's Ranking Data from a given Event

    ADDITIONAL ATTRIBUTES:
    `number`, `team_number` = Team Number of the Corresponding Team"""

    ALIAS = {
        'number': 'team_key',
        'team_number': 'team_key'
    }

    def __number_predicate(self, team_ranking):
        return team_ranking.team_number

    def __sort_order_list(self, raw):
        sort_order_list = [Rank_Sort_Info(raw_value) for raw_value in raw]
        sort_order_return = DataList(objects=sort_order_list, raw=[sort_order.flatten() for sort_order in sort_order_list])
        return sort_order_return

    PREDICATES = {
        'team_number': __number_predicate,
        'number': __number_predicate,
        'sort_order_info': __sort_order_list
    }

    def __repr__(self):
        return '<tbapi.Team_Event_Status_rank: Team {}>'.format(self.team_number)


class Alliance_Backup(Data):
    """Information regarding Backup Swaps during the Elimination Round of an Event"""

    def __repr__(self):
        return '<tbapi.Alliance_Backup>'


class Team_Event_Status_alliance(Data):
    """An Eleminations Alliance at a given Event"""

    def __create_backup(self, raw):
        if raw:
            return Alliance_Backup(raw)
        else:
            return None

    PREDICATES = {
        'backup': __create_backup,
    }

    def __repr__(self):
        return '<tbapi.Team_Event_Status_alliance: Seed {}>'.format(self.number)


class Team_Event_Status_playoff(Data):
    """Information regarding the status of an Eliminations Alliance at a given Event

    ATTRIBUTE ALLIASES:
    `current_level_record` > `current_wlt`, `current_record`
    `playoff_average` > `average`"""

    ALIAS = {
        'current_wlt': 'current_level_record',
        'current_record': 'current_level_record',
        'average': 'playoff_average'
    }

    PREDICATES = {
        'current_level_record': WLT_Record,
        'record': WLT_Record
    }

    def __repr__(self):
        return '<tbapi.Eliminations_Alliance_Status>'


class Team_Event_Status(Data):
    """Information regarding the status of a Team at a given Event"""

    PREDICATES = {
        'qual': Team_Event_Status_rank,
        'alliance': Team_Event_Status_alliance,
        'playoff': Team_Event_Status_playoff
    }

    def __repr__(self):
        return '<tbapi.Team_Event_Status: Team {}>'.format(self.qual.team_number)


class Event_Ranking(Data):
    """Information Regarding Team Rankings at a given Event"""

    def __ranking_list(self, raw):
        ranking_list = [Team_Event_Status_rank(raw_value) for raw_value in raw]
        ranking_return = DataList(objects=ranking_list, raw=[rank.flatten() for rank in ranking_list])
        return ranking_return

    def __sort_order_list(self, raw):
        sort_order_list = [Rank_Sort_Info(raw_value) for raw_value in raw]
        sort_order_return = DataList(objects=sort_order_list, raw=[sort_order.flatten() for sort_order in sort_order_list])
        return sort_order_return

    PREDICATES = {
        'rankings': __ranking_list,
        'sort_order_info': __sort_order_list
    }

    def __repr__(self):
        return '<tbapi.Event_Ranking>'


class Event_District_Points_Team(Data):
    """Information regarding the District Points gained by a specific Team at a given Event"""

    def __repr__(self):
        return '<tbapi.Event_District_Points_Team>'


class Event_District_Points_Tiebreakers(Data):
    """Information regarding the Tiebreaker values specific Team at a given Event"""

    def __repr__(self):
        return '<tbapi.Event_District_Points_Tiebreakers>'


class Event_District_Points(Data):
    """Information regarding the District Points gained by the particiapting Teams of a given Event"""

    def __points_list(self, raw):
        points_list = [Event_District_Points_Team(raw_value) for raw_value in raw]
        points_return = DataList(objects=points_list, raw=[points_value.flatten() for points_value in points_list])
        return points_return

    def __tiebreakers_list(self, raw):
        tiebreaker_list = [Event_District_Points_Tiebreakers(raw_value) for raw_value in raw]
        tiebreaker_return = DataList(objects=tiebreaker_list, raw=[tiebreaker.flatten() for tiebreaker in tiebreaker_list])
        return tiebreaker_return

    PREDICATES = {
        'points': __points_list,
        'tiebreakers': __tiebreakers_list
    }

    def __repr__(self):
        return '<tbapi.Event_District_Points>'


class Event_Insights_2016_Detail(Data):
    """Categorized Insights for FIRST Stronghold qualification and elimination matches"""

    def __repr__(self):
        return '<tbapi.Event_Insights_2016_Detail>'


class Event_Insights_2016(Data):
    """Insights for FIRST Stronghold qualification and elimination matches"""

    PREDICATES = {
        'qual': Event_Insights_2016_Detail,
        'playoff': Event_Insights_2016_Detail
    }

    def __repr__(self):
        return '<tbapi.Event_Insights_2016>'


class Event_Insights_2017_Detail(Data):
    """Categorized Insights for FIRST STEAMWORKS qualification and elimination matches"""

    def __repr__(self):
        return '<tbapi.Event_Insights_2017_Detail>'


class Event_Insights_2017(Data):
    """Insights for FIRST STEAMWORKS qualification and elimination matches"""

    PREDICATES = {
        'qual': Event_Insights_2017_Detail,
        'playoff': Event_Insights_2017_Detail
    }

    def __repr__(self):
        return '<tbapi.Event_Insights_2017>'


class Event_Team_Stat(Data):
    """Information About a Statistic for a Given Team at a given event"""

    def __repr__(self):
        return '<tbapi.Event_Team_Stat: {}>'.format(self.number)


class Event_OPRs(Data):
    """OPR, DPR, and CCWM for all Teams at a given Event"""

    def __repr__(self):
        return '<tbapi.Event_OPRs>'




class Eliminations_Alliance(Data):

    PREDICATES = {
        'backup': Alliance_Backup,
        'status': Team_Event_Status_playoff
    }