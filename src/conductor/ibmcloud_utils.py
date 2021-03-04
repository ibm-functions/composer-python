import json
import os
from enum import Enum


class NamespaceType(Enum):
    IAM = 1
    CF = 2


def get_namespace():
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

    namespace_mode_str = fn_config['WskCliNamespaceMode']
    try:
        namespace_mode = NamespaceType[namespace_mode_str]
    except KeyError as e:
        print(f'Error: Found unknown namespace mode {namespace_mode_str} in functions config.')
        raise e

    return {
        'id': fn_config['WskCliNamespaceId'],
        'mode': namespace_mode
    }


def get_namespace_id():
    return get_namespace()['id']


def get_namespace_mode():
    return get_namespace()['mode']


def get_iam_auth_header():
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

    return ic_config['IAMToken']
