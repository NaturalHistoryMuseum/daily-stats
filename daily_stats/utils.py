# !/usr/bin/env python
# encoding: utf-8

import requests


def make_request(url, **kwargs):
    """
    Wrapper around requests.get that adds the user agent header.
    """
    headers = {'User-Agent': 'NHMUK stats scripts: data [at] nhm.ac.uk'}
    headers.update(kwargs.get('headers', {}))
    return requests.get(url, headers=headers, **kwargs)
