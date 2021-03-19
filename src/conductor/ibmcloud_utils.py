"""
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import json
import os
from enum import Enum
import datetime


class NamespaceType(Enum):
    IAM = 1
    CF = 2


def get_config_functions():
    fn_config_path = os.environ.get(
        'IC_FN_CONFIG_FILE',
        os.path.expanduser('~/.bluemix/plugins/cloud-functions/config.json')
    )

    try:
        with open(fn_config_path) as f:
            fn_config = json.load(f)
    except IOError as e:
        print('Could not open ibmcloud functions plugin config')
        raise e

    return fn_config


def get_namespace_id():
    return get_config_functions()['WskCliNamespaceId']


def get_namespace_mode():
    namespace_mode_str = get_config_functions()['WskCliNamespaceMode']

    try:
        namespace_mode = NamespaceType[namespace_mode_str]
    except KeyError as e:
        print(f'Error: Found unknown namespace mode {namespace_mode_str} in functions config.')
        raise e

    return namespace_mode


def get_config_ibmcloud():
    ic_config_path = os.environ.get(
        'IC_CONFIG_FILE',
        os.path.expanduser('~/.bluemix/config.json')
    )

    try:
        with open(ic_config_path) as f:
            ic_config = json.load(f)
    except IOError as e:
        print('Could not open ibmcloud config')
        raise e

    return ic_config


def get_iam_token():
    return get_config_ibmcloud()['IAMToken']


def get_iam_token_timestamp():
    timestamp =  get_config_functions()['IamTimeTokenRefreshed']

    # Remove colon from UTC time offset string to parse it with strptime's %z
    if timestamp[-3] == ':':
        timestamp = timestamp[:-3] + timestamp[-2:]

    # We remove the tzinfo to allow for comparison with datetime.now() which
    # returns a naive datetime object. Since both timestamps are most likely
    # generated in the same timezone, this should be ok.
    return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)


def iam_token_expired(time_refreshed, time_reference = None):
    if not time_reference:
        time_reference = datetime.datetime.now()

    return time_reference - time_refreshed > datetime.timedelta(hours=1)
