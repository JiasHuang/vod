#!/usr/bin/env python
# coding: utf-8

import re

from .utils import *

VALID_URL = r'nbahdreplay'

def extract(url):
    if url.endswith('com/'):
        return [obj.to_page() for obj in findImageLink(url, ImageExt=None)]
    else:
        return [pageObj(m.group(1)) for m in re.finditer(r'href="(http://telechargementfilmhd.com[^"]*)"', load(url))]

    return None
