#coding: utf-8

__version__ = "0.0.1"
__author__  = "@DFIRENCE | CARLOS DIAZ"
__credits__ = "CERT-BDF TheHive Project Authors"

import json
import sys
import os
import requests
from requests.auth import AuthBase
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# ---
#   This Class is Authored by CERT-BDF
class BearerAuth(AuthBase):
    """
        A custom authentication class for requests

        :param api_key: The API Key to use for the authentication
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, req):
        req.headers['Authorization'] = 'Bearer {}'.format(self.api_key)
        return req

# ---
class TheHiveApi:
    def __init__(self, url, principal, password=None, proxies={}, cert=False):
        self.url        = url
        self.principal  = principal
        self.password   = password
        self.proxies    = proxies
        self.cert       = cert
        self.session    = requests.Session()
        if self.password:
            self.auth = requests.auth.HTTPBasicAuth(self.principal, self.password)
        else:
            self.auth = BearerAuth(self.principal)

    def create_case(self, case):
        restapi = '{0}/{1}/{2}'.format(self.url, 'api', 'case')
        headers = {'Content-Type': 'application/json'}
        data    = json.dumps(case) # <- @DFIRENCE | No JSONIFY Object | STD LIB JSON DUMPS
        try:
            http = requests.post(restapi, headers=headers, data=data, proxies=self.proxies, auth=self.auth, verify=self.cert)
            if http.status_code == 201:
                return json.loads(http.content)
            else:
                print "{0}:  {1}".format(http.status_code, http.reason)
        except requests.exceptions.RequestException as http_error:
            msg = '[!] Case Creation Error:  Request Failed {}'.format(http_error)
            raise msg

# ---
    def create_observable(self, case_id, observable):
        restapi = '{0}/{1}/{2}/{3}/{4}'.format(self.url, 'api', 'case', case_id, 'artifact')
        headers = {'Content-Type': 'application/json'}
        data    = json.dumps(observable)
        try:
            http = requests.post(restapi, headers=headers, data=data, proxies=self.proxies, auth=self.auth, verify=self.cert)
            '''
            http = self.session..post(restapi, headers=headers, data=data, proxies=self.proxies, auth=self.auth, verify=self.cert)
            '''
            if http.status_code == 201:
                return http
            else:
                return (http.status_code, http.reason, http.content)
        except requests.exceptions.RequestException as e:
            raise e
