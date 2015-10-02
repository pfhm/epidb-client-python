#!/usr/bin/env python

import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'src'))

from datetime import datetime, date

from epidb_client import EpiDBClient

import config

api_key = config.api_key
user_id = config.user_id
survey_id = config.survey_id
answers = {'q1': 1,
           'q2': True,
           'q3': [ 1, 2, 3 ],
           'q4': 'Jakarta',
           'q5': date(2011, 01, 01),
           'q6': datetime(2011, 01, 01, 12, 34, 31),
           }

# If you set date to None, the current date and time 
# will be used
#   date = None
date = datetime(2009, 12, 15, 1, 2, 3)

client = EpiDBClient(api_key)
client.server = config.server # Use this if you want to override
                              # the server location
result = client.response_submit(user_id, survey_id, answers, date)

status = result['stat']

print "status:", status

if status == 'ok':
    print "id:", result['id']
else:
    print "error code:", result['code']
    print "       msg:", result['msg']

