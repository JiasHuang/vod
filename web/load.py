#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib

import page
import meta

from mod_python import util, Cookie

def getUnparsedURL(req):
    m = re.search(r'=(.*)$', req.unparsed_uri, re.DOTALL)
    if m:
        return urllib.unquote(m.group(1))
    return None

def index(req):

    req.content_type = 'text/html; charset=utf-8'
    form = req.form or util.FieldStorage(req)

    p = form.get('p', None) # page
    q = form.get('q', None) # query
    s = form.get('s', None) # search
    x = form.get('x', None) # extra

    if q:
        page.search(req, q, s, x)

    elif p:
        p = getUnparsedURL(req) or p
        page.page_core(req, p)

    return

