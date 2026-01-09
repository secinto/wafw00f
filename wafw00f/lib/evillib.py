#!/usr/bin/env python3
'''
Copyright (C) 2024, WAFW00F Developers.
See the LICENSE file for copying permission.
'''

import time
import logging
from copy import copy

import requests
import urllib3

# For requests < 2.16, this should be used.
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# For requests >= 2.16, this is the convention
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Accept-Language': 'en-US,en;q=0.5',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Priority': 'u=0, i',
    'DNT': '1',
}
proxies = {}

class waftoolsengine:
    def __init__(
        self, target='https://example.com', debuglevel=0,
        path='/', proxies=None, redir=True, head=None, timeout=7, debug=False
    ):
        self.target = target
        self.debuglevel = debuglevel
        self.requestnumber = 0
        self.path = path
        self.redirectno = 0
        self.allowredir = redir
        self.proxies = proxies
        self.log = logging.getLogger('wafw00f')
        self.timeout = timeout
        self.debug = debug
        if head:
            self.headers = head
        else:
            self.headers = copy(def_headers) #copy object by value not reference. Fix issue #90

    def Request(self, headers=None, path=None, params={}, delay=0):
        try:
            time.sleep(delay)
            if not headers:
                h = self.headers
            else: h = headers

            if self.debug:
                print('\n' + '=' * 60)
                print('>>> REQUEST #%d' % (self.requestnumber + 1))
                print('=' * 60)
                print('URL: %s' % self.target)
                print('Method: GET')
                if params:
                    print('Params: %s' % params)
                print('Headers:')
                for key, val in h.items():
                    print('  %s: %s' % (key, val))

            req = requests.get(self.target, proxies=self.proxies, headers=h, timeout=self.timeout,
                    allow_redirects=self.allowredir, params=params, verify=False)

            if self.debug:
                print('\n' + '-' * 60)
                print('<<< RESPONSE')
                print('-' * 60)
                print('Status: %d %s' % (req.status_code, req.reason))
                print('Headers:')
                for key, val in req.headers.items():
                    print('  %s: %s' % (key, val))
                print('Body (first 500 chars):')
                print(req.text[:500] if len(req.text) > 500 else req.text)
                print('=' * 60 + '\n')

            self.log.info('Request Succeeded')
            self.log.debug('Headers: %s\n' % req.headers)
            self.log.debug('Content: %s\n' % req.content)
            self.requestnumber += 1
            return req
        except requests.exceptions.RequestException as e:
            self.log.error('Something went wrong %s' % (e.__str__()))
