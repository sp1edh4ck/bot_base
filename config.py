"""
This file describes the functionality for
using data from the .env file.

CLEAR_LIST and ADMIN_IDS are needed to convert
a string with the admin ids to a list of admin ids.

Example:
ADMIN_IDS = '100000, 100001, 100002,'
CLEAR_LIST = [i for i in re.split(',', os.getenv('ADMIN_IDS')) if i]
ADMIN_IDS = [int(i) for i in CLEAR_LIST]

Result:
ADMIN_IDS = [100000, 100001, 100002]

It is mandatory to put a comma at the end of the line with the administrators' id.
"""


import os
import re

from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv('DB_PASSWORD')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CLEAR_LIST = [i for i in re.split(',', os.getenv('ADMIN_IDS')) if i]
ADMIN_IDS = [int(i) for i in CLEAR_LIST]
IP = os.getenv('IP')
MAIN_SUPPORT = {
    'id': int(os.getenv('MAIN_SUPPORT')),
    'username': None
}
