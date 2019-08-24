#!/usr/bin/env python
# coding: utf-8

import re
import json

from .utils import *

VALID_URL = r'cctv\.com'

def extract(url):
    objs = []
    txt = load(url)
    for m in re.finditer(r'var jsonData\d*=(.*?);', txt, re.DOTALL | re.MULTILINE):
        ctx = '{"list":%s}' %(re.sub('\'', '"', m.group(1)))
        try:
            data = json.loads(ctx)
            for d in data['list']:
                url, title, img = darg(d, 'url', 'title', 'img')
                objs.append(entryObj(url, title, img))
        except:
            log('Exception:\n'+str(data))

    return objs
