#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import xurl

def getSource(dataLink):
    url = 'http://play.wtutor.net/wp-admin/admin-ajax.php?action=ts-ajax&p=%s&n=1' %dataLink
    txt = xurl.load(url)
    videos = re.findall('file\s*:\s*[\"\']([^\"\']+).+?label\s*:\s*[\"\'](\d+)p[^\}]', txt)
    if videos:
        return videos[0][0]
    return None

