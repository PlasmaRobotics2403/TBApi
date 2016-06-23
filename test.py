
from TBAPythonAPI import *

data = TBAParser(2403, "tester", 1)
print("---- TEST OUTPUT BEGINS HERE ----")
scraper = TBAParser('2403', 'scraper', 1)
teams = scraper.get_team_list()
state_list = {}

for team in teams:
    if team.country_name == "USA":
        if not team.region in state_list:
            state_list[team.region] = 1
        else:
            state_list[team.region] = state_list[team.region] + 1
#print(state_list)
conversion = {'AL': 'Alabama',
                'AK' : 'Alaska',
                'AZ' : 'Arizona',
                'AR' : 'Arkansas',
                'CA' : 'California',
                'CO' : 'Colorado',
                'CT' : 'Connecticut',
                'DE' : 'Delaware',
                'FL' : 'Florida',
                'GA' : 'Georgia',
                'HI' : 'Hawaii',
                'ID' : 'Idaho',
                'IL' : 'Illinois',
                'IN' : 'Indiana',
                'IA' : 'Iowa',
                'KS' : 'Kansas',
                'KY' : 'Kentucky',
                'LA' : 'Louisiana',
                'ME' : 'Maine',
                'MD' : 'Maryland',
                'MA' : 'Massachusetts',
                'MI' : 'Michigan',
                'MN' : 'Minnesota',
                'MS' : 'Mississippi',
                'MO' : 'Missouri',
                'MT' : 'Montana',
                'NE' : 'Nebraska',
                'NV' : 'Nevada',
                'NH' : 'New Hampshire',
                'NJ' : 'New Jersey',
                'NM' : 'New Mexico',
                'NY' : 'New York',
                'NC' : 'North Carolina',
                'ND' : 'North Dakota',
                'OH' : 'Ohio',
                'OK' : 'Oklahoma',
                'OR' : 'Oregon',
                'PA' : 'Pennsylvania',
                'PR' : 'Puerto Rico',
                'RI' : 'Rhode Island',
                'SC' : 'South Carolina',
                'SD' : 'South Dakota',
                'TN' : 'Tennessee',
                'TX' : 'Texas',
                'UT' : 'Utah',
                'VT' : 'Vermont',
                'VA' : 'Virginia',
                'WA' : 'Washington',
                'WV' : 'West Virginia',
                'WI' : 'Wisconsin',
                'WY' : 'Wyoming',
                'DC' : 'District of Columbia'
                }
filtered_list = {}
for state in state_list:
    if not len(state) == 2:
        filtered_list[state] = state_list[state]
#print(filtered_list)
for state in state_list:
    if len(state) == 2:
        state_name = conversion[state]
        filtered_list[state_name] = filtered_list[state_name] + state_list[state]

organized_list = sorted(filtered_list.items(), key=lambda x: x[1], reverse=True)

ranking = 0
none_count = 0

for value in organized_list:
    if not value[0] is None:
        valranking = ranking
        ranking = ranking + 1

        if ranking < 10:
            sanity_marker = " "
        else:
            sanity_marker = ""

        country = value[0]
        teams = value[1]
        print("#" + str(ranking) + sanity_marker + " - " + country + " : " + str(teams))
    else:
        none_count = value[1]

print("----- TEST OUTPUT ENDS HERE -----")
