#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import xurl

def getSource(url, ref=None):
    txt = xurl.load2(url, ref=ref)
    videoURL = re.search('<video .*? src="([^"]*)"', txt)
    if videoURL:
        return videoURL.group(1)
    return None

