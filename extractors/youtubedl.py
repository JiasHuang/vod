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

import xarg
import xdef
import xurl

def redirectURL(url):
    if re.search(r'youku', url):
        url = re.sub('player.youku.com/embed/', 'v.youku.com/v_show/id_', url)
    return url

def getFormat(url):
    formats = []
    m = re.search(r'^(\d+)p($)', xarg.ytdlfmt, re.IGNORECASE)
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
        formats.append(xarg.ytdlfmt)
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
                local = xdef.workdir+'vod_list_'+hashlib.md5(path).hexdigest()+'.m3u'
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

def extractPlayList(local, url):
    txt = xurl.readLocal(url)
    times = []
    links = []
    descs = []

    for m in re.finditer(r'EXTINF:\s*(.*?),\s*(.*?)\n(.*?)\n', txt, re.DOTALL|re.MULTILINE):
        time, desc, link = m.group(1), m.group(2), m.group(3)
        times.append(time)
        links.append(link)
        descs.append(desc)

    for index,link in enumerate(links):
        src, cookies = extractURL(link)
        time = times[index]
        desc = descs[index]
        if src:
            if not os.path.exists(local):
                fd = open(local, 'w')
                fd.write('#EXTM3U\n')
                fd.write('#EXTINF:%s, %s\n' %(time, desc))
                fd.write(src+'\n')
                fd.close()
            else:
                fd = open(local, 'a')
                fd.write('#EXTINF:%s, %s\n' %(time, desc))
                fd.write(src+'\n')
                fd.close()

    if not os.path.exists(local):
        fd = open(local, 'w')
        fd.write('#EXTM3U\n')
        fd.close()

    return

def extractURL(url, key=None, ref=None, dontParseJson=False):

    print('\n[ytdl][extractURL]\n')

    url = redirectURL(url)
    arg = '-i -j --no-playlist --no-warnings'
    fmt = getFormat(url)
    local = xdef.workdir+'vod_list_'+hashlib.md5(url+fmt).hexdigest()+'.json'

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

    cmd = '%s -f \'%s\' --user-agent \'%s\' %s \'%s\' > %s' %(xdef.ytdlcmd(), fmt, xurl.defvals.ua, arg, url, local)

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

def extractSUB(url):

    if not url or not re.search(r'youtube.com/watch\?v=', url):
        return None

    print('\n[ytdl][extracSUB]\n')

    sub = 'vod_sub_'+hashlib.md5(url).hexdigest()

    for files in os.listdir(xdef.workdir):
        if files.startswith(sub):
            print('\tsub: '+xdef.workdir+files)
            return files

    try:
        opt = ''
        if xarg.autosub == 'yes':
            opt += '--write-auto-sub '
        cmd = '%s %s %s -o %s%s \'%s\'' %(xdef.ytdlcmd(), xdef.ytdlsub, opt, xdef.workdir, sub, url)

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

