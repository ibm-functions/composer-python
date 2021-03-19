import os
import datetime
import pytest

from conductor.conductor import openwhisk
from conductor.ibmcloud_utils import (
    get_iam_token_timestamp,
    iam_token_expired
)

fn_config_path = os.environ.get(
    'IC_FN_CONFIG_FILE',
    os.path.expanduser('~/.bluemix/plugins/cloud-functions/config.json')
)

ic_config_path = os.environ.get(
    'IC_CONFIG_FILE',
    os.path.expanduser('~/.bluemix/config.json')
)


class TestIamTokenExpireCheck:
    def test_read_timestamp(self, fs):
        fs.create_file(
            fn_config_path,
            contents='{ "IamTimeTokenRefreshed": "2021-03-15T13:24:14+01:00" }'
        )
        timestamp = get_iam_token_timestamp()
        assert timestamp == datetime.datetime(2021, 3, 15, 13, 24, 14)

    def test_read_timestamp_tz_ignored(self, fs):
        fs.create_file(
            fn_config_path,
            contents='{ "IamTimeTokenRefreshed": "2021-03-15T13:24:14+06:00" }'
        )
        timestamp = get_iam_token_timestamp()
        assert timestamp == datetime.datetime(2021, 3, 15, 13, 24, 14)

    def test_not_expired(self):
        time_refreshed = datetime.datetime(2021, 3, 15, 13, 24, 14)
        time_reference = datetime.datetime(2021, 3, 15, 13, 30, 0)
        token_expired = iam_token_expired(time_refreshed, time_reference)
        assert token_expired == False

    def test_expired(self):
        time_refreshed = datetime.datetime(2021, 3, 15, 13, 24, 14)
        time_reference = datetime.datetime(2021, 3, 15, 14, 25, 0)
        token_expired = iam_token_expired(time_refreshed, time_reference)
        assert token_expired == True

    def test_conductor_fails_when_token_expired(self, fs):
        fs.create_file(
            ic_config_path,
            contents='{ "IAMToken": "some-token" }')

        fs.create_file(
            fn_config_path,
            contents='''
{
    "IamTimeTokenRefreshed": "2021-03-14T12:00:00+01:00",
    "WskCliNamespaceId": "some-namespace-id",
    "WskCliNamespaceMode": "IAM"
}
'''
        )

        with pytest.raises(Exception) as e:
            openwhisk({})

        assert 'IAM token seems to be expired' in str(e)
