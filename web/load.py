#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

import page
import xurl

from mod_python import util, Cookie

def getUnparsedURL(req):
    m = re.search(r'=(.*)$', req.unparsed_uri, re.DOTALL)
    if m:
        return xurl.unquote(m.group(1))
    return None

def index(req):

    req.content_type = 'text/html; charset=utf-8'
    form = req.form or util.FieldStorage(req)

    p = form.get('p', None) # page
    q = form.get('q', None) # query
    d = form.get('d', None) # dir
    s = form.get('s', None) # search
    x = form.get('x', None) # extra

    if p:
        xurl.init(logfile='vod-page.log')
        p = getUnparsedURL(req) or p
        req.write(page.getPageJSON(p))

    elif q:
        xurl.init(logfile='vod-page-search.log')
        req.write(page.getSearchJSON(q, s, x))

    elif d:
        req.write(page.getDIRJSON(d))

    return

