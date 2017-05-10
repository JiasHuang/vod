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
    for r in result:
        fd.write('#EXTINF:-1,0\n')
        fd.write(r+'\n')
    fd.close()
    return local

def parseJson(path):

    print('\n[ytdl][parseJson]\n')

    results = []
    cookies = None

    fd = open(path, "r")
    lines = fd.readlines()
    fd.close()

    for line in lines:

        try:
            data = json.loads(line)
            urls = data['url']
        except:
            print('\texception')
            continue

        try:
            cookies = data['http_headers']['Cookie'].encode('utf8')
        except:
            cookies = None

        if not isinstance(urls, basestring):
            results.append(urls)
        else:
            encoded = re.search(r'data:application/vnd.apple.mpegurl;base64,([a-zA-Z0-9+/=]*)', urls)
            if encoded:
                local = xdef.workdir+'vod_list_'+hashlib.md5(path).hexdigest()+'.m3u'
                decoded = base64.b64decode(encoded.group(1))
                xurl.saveLocal(local, decoded)
                results.append(local)
            else:
                results.append(urls)

    if len(results) == 0:
        print('\tNo results')
        return None, None
    elif len(results) == 1:
        print('\tret : %s' %(results[0]))
        print('\thdr : %s' %(cookies or ''))
        return results[0], cookies
    else:
        m3u = genM3U(path, results)
        print('\tret : %s' %(m3u))
        print('\thdr : %s' %(cookies or ''))
        return m3u, cookies

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
        cmd = '%s --sub-lang=en,en-US,en-GB,en-AU,en-CA --write-sub --write-auto-sub --skip-download -o %s%s \'%s\'' %(xdef.ytdl, xdef.workdir, sub, url)
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

