import json
import os


def get_namespace():
    fn_config_path = os.environ.get(
        'IC_FN_CONFIG_FILE',
        os.path.expanduser('~/.bluemix/plugins/cloud-functions/config.json')
    )

    try:
        with open(fn_config_path) as f:
            fn_config = json.load(f)
    except IOError as e:
        print('Error: Could not open ibmcloud functions plugin config.')
        raise e

    return {
        'id': fn_config['WskCliNamespaceId'],
        'mode': fn_config['WskCliNamespaceMode']
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
        print('Error: Could not open ibmcloud config.')
        raise e

    return ic_config['IAMToken']
