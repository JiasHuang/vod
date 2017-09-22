#!/usr/bin/env python
# -*- coding: utf-8 -*-

import page
import meta

from mod_python import util, Cookie

def index(req):

    req.content_type = 'text/html; charset=utf-8'
    form = req.form or util.FieldStorage(req)

    q = form.get('q', None) # query
    s = form.get('s', None) # search
    x = form.get('x', None) # extra

    if q:
        page.search(req, q, s, x)

    return

