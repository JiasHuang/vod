#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import base64
import hashlib

import xurl
import jsunpack

def checkURL(url):
    site = xurl.findSite(url)
    return re.compile('(jav)').search(site)

def checkVideoURL(url):
    site = xurl.findSite(url)
    return re.compile('(openload|drive.google|bitporno)').search(site)

def load(url, local=None, options=None):
    return xurl.load2(url, local, options)

def getSource(url):
    links = xurl.getIFrame(url)
    for link in links:
        if checkVideoURL(link):
            return link
    return None

