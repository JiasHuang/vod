#!/usr/bin/env python
# coding: utf-8

import re

import xurl
from .utils import *

VALID_URL = r'today\.line\.me'

def extract(url):
    if re.search(r'api.today.line.me', url):
        link = re.search(r'"720":"([^"]*)"', xurl.curl(url, cache=False))
        if link:
            return [entryObj(link[1])]
    else:
        programId = re.search(r'data-programId="([^"]*)"', xurl.curl(url, cache=False))
        if programId:
            link = 'https://api.today.line.me/webapi/linelive/' + programId[1]
            return [pageObj(link)]
        else:
            return [obj.to_page() for obj in findImageLink(url, ImageExt=None, ImagePattern=r'url\((.*?)\)')]

    return None
