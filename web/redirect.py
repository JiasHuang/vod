#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from mod_python import util, Cookie

def index(req):

    req.content_type = 'text/html; charset=utf-8'
    form = req.form or util.FieldStorage(req)

    i = form.get('i', None) # input

    if i:
        i = i.strip()
        if i.startswith('#'):
            util.redirect(req, 'index.html?c='+i[1:])
        elif i.startswith('http'):
            util.redirect(req, 'index.html?v='+i)
        elif i.startswith('/') and os.path.isdir(i):
            util.redirect(req, 'list.html?d='+i)
        elif i.startswith('/') and os.path.exists(i):
            util.redirect(req, 'index.html?f='+i)
        else:
            util.redirect(req, 'search.html?q='+re.sub('\s+', ' ', i))

    return

