#!/usr/bin/env python

import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'src'))

from epidb_client import EpiDBClient

import config

api_key = config.api_key
user_id = config.user_id
profile_survey_id = config.profile_survey_id
answers = {'birth-place': 'Jakarta',
           'birth-day': '2009-09-09',
           'has-pets': False}

# if you set date to none, the current date and time 
# will be used
#   date = none
date = datetime(2009, 12, 15, 1, 2, 3)

client = EpiDBClient(api_key)
client.server = config.server # Use this if you want to override
                              # the server location
result = client.profile_update(user_id, profile_survey_id, answers, date)

status = result['stat']

print "status:", status

if status == 'ok':
    print "id:", result['id']
else:
    print "error code:", result['code']
    print "       msg:", result['msg']

