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

import xurl

class defvals:
    ytdlsub  = '--no-warnings --write-sub --skip-download --sub-lang=en,en-US'
    ua = xurl.defvals.ua

def ytdlcmd():
    if os.path.exists('/usr/bin/python3'):
        for f in ['/usr/local/bin/youtube-dl', os.path.expanduser('~/bin/youtube-dl')]:
            if os.path.exists(f):
                return 'python3 ' + f
    return 'youtube-dl'

def redirectURL(url):
    if re.search(r'youku', url):
        url = re.sub('player.youku.com/embed/', 'v.youku.com/v_show/id_', url)
    return url

def getFormat(url, fmt):
    formats = []
    m = re.search(r'^(\d+)p($)', fmt, re.IGNORECASE)
    if m:
        h = int(m.group(1))
        if h >= 1080:
            formats.append('37')
        if h >= 720:
            formats.append('22')
        if h >= 480:
            formats.append('59')
            formats.append('35')
        if h >= 360:
            formats.append('18')
            formats.append('34')
        formats.append('best[ext!=webm][protocol^=http][height<=%s]' %(h))
        formats.append('best[ext!=webm][height<=%s]' %(h))
    else:
        formats.append(fmt)
    formats.append('best[ext!=webm]')
    return '/'.join(formats)

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
                local = xurl.genLocal(path, prefix='vod_list_', suffix='.m3u')
                decoded = base64.b64decode(encoded.group(1))
                xurl.saveLocal(local, decoded)
                results.append(local)
            else:
                results.append(urls)

    if cookies:
        print('\thdr : %s' %(cookies))

    if len(results) == 0:
        print('\tNo results')
        return None, None
    elif len(results) == 1:
        print('\tret : %s' %(results[0]))
        return results[0], cookies
    else:
        m3u = xurl.genLocal(path, prefix='vod_list_', suffix='.m3u8')
        xurl.saveM3U8(m3u, results)
        print('\tret : %s' %(m3u))
        return m3u, cookies

def extractURL(url, fmt, key=None, ref=None, dontParseJson=False):

    print('\n[ytdl][extractURL]\n')

    url = redirectURL(url)
    arg = '-i -j --no-playlist --no-warnings'
    fmt = getFormat(url, fmt)
    local = xurl.genLocal(url+fmt, prefix='vod_list_', suffix='.json')

    if key:
        arg = ' '.join([arg, '--video-password='+key])

    if ref and ref != url:
        arg = ' '.join([arg, '--referer=\'%s\'' %(ref)])

    print('\targ : %s' %(arg or ''))
    print('\tfmt : %s' %(fmt or ''))

    if os.path.exists(local) and not xurl.checkExpire(local):
        print('\tret : %s' %(local))
        if dontParseJson:
            return local
        return parseJson(local)

    cmd = '%s -f \'%s\' --user-agent \'%s\' %s \'%s\' > %s' %(ytdlcmd(), fmt, defvals.ua, arg, url, local)

    try:
        start_time = timeit.default_timer()
        output = subprocess.check_output(cmd, shell=True)
        elapsed = timeit.default_timer() - start_time
    except:
        elapsed = timeit.default_timer() - start_time
        print('\texception')
        return None

    print('\tsec : %s' %(str(elapsed)))
    print('\tret : %s' %(local))

    if dontParseJson:
        return local

    return parseJson(local)

def extractSUB(url, autosub=None):

    if not url or not re.search(r'youtube.com/watch\?v=', url):
        return None

    print('\n[ytdl][extracSUB]\n')

    sub = xurl.genLocal(url, prefix='vod_sub_')
    sub_dir = os.path.dirname(sub)

    for f in os.listdir(sub_dir):
        if f.startswith(sub):
            print('\tsub: '+sub_dir+f)
            return f

    try:
        opt = ''
        if autosub == 'yes':
            opt += '--write-auto-sub '
        cmd = '%s %s %s -o %s \'%s\'' %(ytdlcmd(), defvals.ytdlsub, opt, sub, url)

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

