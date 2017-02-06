#!/usr/bin/env python
# -*- coding: utf-8 -*-

import esl

from mod_python import util

def index(req):
    req.content_type = 'text/html; charset=utf-8'
    arg  = util.FieldStorage(req)
    k    = arg.get('k', None)
    esl.outDB(req, k)
    return

