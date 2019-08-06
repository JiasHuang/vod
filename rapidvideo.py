#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xurl

def getSource(url, ref=None):
    txt = xurl.curl(url, ref=ref)
    videoURL = re.search('<source.*? src="([^"]*)"', txt)
    if videoURL:
        return videoURL.group(1)
    return None

