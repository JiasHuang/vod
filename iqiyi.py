#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import hashlib
import urllib

import xdef
import xurl

def genM3U(url, result):
    local = xdef.workdir+'vod_list_'+hashlib.md5(url).hexdigest()+'.m3u'
    fd = open(local, 'w')
    fd.write('#EXTM3U\n')
    for r in result:
        fd.write('#EXTINF:-1,0\n')
        fd.write(r+'\n')
    fd.close()
    return local

def getSource(url):
    # cache.video.iqiyi.com/jp/dash? => data.video.iqiyi.com/videos/ =>  https://v-*
    results = []
    data_prefix = 'https://data.video.iqiyi.com/videos'
    txt = xurl.load2(url, cache=False)
    for m in re.finditer(r'"l":"(.*?)"', txt):
        data_url = data_prefix + re.sub('\\\\', '', m.group(1))
        data_txt = xurl.load2(data_url, cache=False)
        for l in re.finditer(r'"l":"(.*?)"', data_txt):
            results.append(l.group(1))
    return genM3U(url, results)

