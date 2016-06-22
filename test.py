
from TBAPythonAPI import *

data = TBAParser(2403, "tester", 1)
print("TEST OUTPUT:")
print(data.find_event_key(2016, 'Arizona S'))
