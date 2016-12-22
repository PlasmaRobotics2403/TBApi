# TBApi - Python Library for the TBA API v2

TBApi is a Python Library for connection to the Blue Alliance API v2, programmed by members of [FRC Team 2403 Plasma Robotics](www.plasmarobotics.com).  Through use of TBApi, programmers can easily gather information regarding FRC Teams and Events for use in their own programming, thanks to data provided by The Blue Alliance.

## Installation
TBApi is installed simply through the use of PIP:
```
pip install tbapi
```

## Usage
To import TBApi, simply import the module. No `from` or `as` trickery is needed in order to properly set it up, and importing the module will import both the Parser and Data Classes that will make data manipulation easy.
```python
import tbapi
```

To create a parser object:
```python
parser = tbapi.TBAParser(team_number, usage_string, version_number)
```
This parser object is required because The Blue Alliance API requires certain information in order to connect to and use the API.  `team_number` is an integer number representing the team who is primarily using or operating the script.  `usage_string` is a simple description of the usage case.  `version_number` is a string containing the version number of the script (aka `1.2.32` or something along those lines).  These values allow TBA to know who and what is causing issues if they arise (aka API spamming or something similar).

In order to pull data from TBA, you must use a sub-method of your parser object.  These sub-methods can be found with better documentation on the wiki.  Here, we will work with a simple sub-method that simply pulls a specific team object.
```python
team = parser.get_team('frc2403')
# The string passed into this function is a team key, not a team number.
# This is documented on the wiki, but know that simply passing in a team number will not work by default at this point in time.
```
This method will return a `TBATeam` object.  From this object, subatributes can be called to get further information.  For example, to get the team's motto, one could call `team.motto`.

All methods return standard objects, such as `TBATeam` or `TBAEvent` which are documented more fully on the wiki and provide access to specific attributes acourding to the specification of the TBA API as documented on their site.  Methods that return multiple of these standard objects will do so in list form, and one can interate through said list to access all Standard Objects.

---
For more detailed information, see the Wiki.
