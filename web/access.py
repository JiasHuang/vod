#!/usr/bin/env python

import re

import xurl

from mod_python import util

def getUnparsedURL(req):
    m = re.search(r'=(.*)$', req.unparsed_uri, re.DOTALL)
    if m:
        return xurl.unquote(m.group(1))
    return None

def index(req):

    arg  = util.FieldStorage(req)
    j    = arg.get('j', None) # json

    if j:
        req.content_type = 'application/json'
        j = getUnparsedURL(req) or j
        req.write(xurl.curl(j))
        return

    return

