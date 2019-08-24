#!/usr/bin/env python
# coding: utf-8

import re
import json

from .utils import *

VALID_URL = r'api\.cntv\.cn'

def extract(url):
    objs = []
    txt = load(url)
    try:
        data = json.loads(txt)
        for d in data['list']:
            name, photo, url = darg(d, 'name', 'video_album_photo_url', 'video_album_url')
            objs.append(entryObj(url, name, photo, video=False))
    except:
        log('Exception:\n'+txt)

    return objs
