#  Copyright (c) 2020 Xavier Baró
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
""" TeSLA CE API global tests """
import pytest
import json


@pytest.mark.django_db
def test_favicon(rest_api_client):
    favicon_resp = rest_api_client.get('/favicon.ico')
    assert favicon_resp.status_code == 302


@pytest.mark.django_db
def test_api_version(rest_api_client):
    api_version_resp = rest_api_client.get('/api/version/')
    assert api_version_resp.status_code == 200
    assert 'version' in json.loads(api_version_resp.content)

    lapi_version_resp = rest_api_client.get('/lapi/version/')
    assert lapi_version_resp.status_code == 200
    assert 'version' in json.loads(lapi_version_resp.content)

    assert json.loads(api_version_resp.content)['version'] == json.loads(lapi_version_resp.content)['version']


