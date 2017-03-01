#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import hashlib
import json
import time
import base64

import timeit
import xdef
import xurl

def checkURL(url):
    site = xurl.findSite(url)
    return re.compile('(youtube|dailymotion|facebook|bilibili|vimeo|youku|openload|litv|drive|iqiyi|letv)').search(site)

def redirectURL(url):
    if re.search(r'youku', url):
        url = re.sub('player.youku.com/embed/', 'v.youku.com/v_show/id_', url)
    return url

def parseParameters(url):
    match = re.search(r'(.*?)&ytdl_password=(.*?)$', url)
    if match:
        url = match.group(1)
        return '--video-password ' + match.group(2)
    return None

def getFmt(url):
    return xdef.ytdlfmt

def genM3U(url, result):
    local = xdef.workdir+'vod_list_'+hashlib.md5(url).hexdigest()+'.m3u'
    fd = open(local, 'w')
    fd.write('#EXTM3U\n')
    fd.write('#EXT-X-TARGETDURATION:0\n')
    for r in result:
        fd.write('#EXTINF:0,0\n')
        fd.write(r+'\n')
    local.close()
    return local

def parseJson(path):

    print('\n[ytdl][parseJson]\n')

    data = json.loads(xurl.readLocal(path))

    try:
        results = data['url']
    except:
        print('\texception')
        return None, None

    try:
        cookies = data['http_headers']['Cookie'].encode('utf8')
    except:
        cookies = None

    if not isinstance(results, basestring):
        results = genM3U(url, results)
    else:
        encoded = re.search(r'data:application/vnd.apple.mpegurl;base64,([a-zA-Z0-9+/=]*)', results)
        if encoded:
            local = xdef.workdir+'vod_list_'+hashlib.md5(path).hexdigest()+'.m3u'
            decoded = base64.b64decode(encoded.group(1))
            xurl.saveLocal(local, decoded)
            results = local

    print('\tret : %s' %(results or ''))
    print('\thdr : %s' %(cookies or ''))
    return results, cookies

def extractURL(url):

    print('\n[ytdl][extractURL]\n')

    url = redirectURL(url)
    arg = parseParameters(url)
    fmt = getFmt(url)
    local = xdef.workdir+'vod_list_'+hashlib.md5(url+fmt).hexdigest()+'.json'

    if arg:
        print('\targ : %s' %(arg or ''))

    if fmt:
        print('\tfmt : %s' %(fmt or ''))

    if os.path.exists(local) and not xurl.checkExpire(local):
        print('\tret : %s' %(local))
        return parseJson(local)

    cmd = '%s -f \"%s\" -j --no-playlist %s \'%s\'' %(xdef.ytdl, fmt, arg or '', url)

    try:
        start_time = timeit.default_timer()
        output = subprocess.check_output(cmd, shell=True)
        elapsed = timeit.default_timer() - start_time
    except:
        print('\texception')
        return None, None

    print('\tsec : %s' %(str(elapsed)))
    print('\tret : %s' %(local))

    xurl.saveLocal(local, output)
    return parseJson(local)

def extractSUB(url):

    if not url or not re.search(r'youtube.com', url):
        return None

    print('\n[ytdl][extracSUB]\n')

    sub = 'vod_sub_'+hashlib.md5(url).hexdigest()

    for files in os.listdir(xdef.workdir):
        if files.startswith(sub):
            print('\tsub: '+xdef.workdir+files)
            return files

    try:
        cmd = '%s --sub-lang=en --write-sub --skip-download -o %s%s \'%s\'' %(xdef.ytdl, xdef.workdir, sub, url)
        start_time = timeit.default_timer()
        output = subprocess.check_output(cmd, shell=True)
        elapsed = timeit.default_timer() - start_time
        print('\tsec: '+str(elapsed))
    except:
        print('\texception')
        return None

    m = re.search(r'Writing video subtitles to: (.*)', output)
    if m:
        local = m.group(1)
        print('\tsub: '+local)
        return local

    return None

