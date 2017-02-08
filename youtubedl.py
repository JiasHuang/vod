#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import hashlib
import json
import urlparse
import time

import timeit
import xdef
import xurl

def checkURL(url):
    site = xurl.findSite(url)
    return re.compile('(youtube|dailymotion|facebook|bilibili|vimeo|youku|openload|litv|drive)').search(site)

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
    for s in ['all', 'litv', 'youtube']:
        fmt = xdef.getConf(s)
        if fmt:
            if s == 'all' or re.search(s, url):
                return fmt
    return 'mp4'

def saveCookies(url, rawdata):
    local = xdef.cookies
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    expire = str(int(time.time())+20000)
    fd = open(local, 'w')
    for r in rawdata.split(';'):
        m = re.search(r'\s*([^=]*)=(.*?)$', r)
        if m:
            fd.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(domain, 'TRUE', '/', 'FALSE', expire, m.group(1), m.group(2)))
    fd.close()
    xurl.saveLocal(rawdata, xdef.cookiex)

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

    data = json.loads(xurl.readLocal(path))

    print('\n[ytdl][parseJson]\n')
    print('\tpath: '+path)

    try:
        result = data['url']
    except:
        print('\tret: no url')
        return None

    try:
        cookies = data['http_headers']['Cookie'].encode('utf8')
        print('\tcookies: '+cookies+'\n')
    except:
        cookies = None
        print('\tret: no cookies')

    if cookies:
        saveCookies(result, cookies)

    if isinstance(result, basestring):
        print('\tsrc: '+result+'\n')
        return result

    m3u = genM3U(url, result)
    print('\tsrc: '+m3u+'\n\n')
    return m3u

def extractURL(url):

    print('\n[ytdl][extractURL]\n')
    print('\turl: '+url)

    url = redirectURL(url)
    arg = parseParameters(url)
    ret = xdef.workdir+'vod_list_'+hashlib.md5(url).hexdigest()+'.json'

    if arg:
        print('\targ: '+arg)

    if os.path.exists(ret) and not xurl.checkExpire(ret):
        print('\tret: '+ret)
        return parseJson(ret)

    fmt = getFmt(url)
    print('\tfmt: '+fmt)

    cmd = '%s -f \"%s\" -j --no-playlist %s \'%s\'' %(xdef.ytdl, fmt, arg or '', url)

    try:
        start_time = timeit.default_timer()
        output = subprocess.check_output(cmd, shell=True)
        elapsed = timeit.default_timer() - start_time
        print('\tsec: '+str(elapsed))
    except:
        print('\tret: exception')
        return None

    xurl.saveLocal(output, ret)
    print('\tret: '+ret)
    return parseJson(ret)

def extractURL2(url):
    lists = []
    m3u = extractURL(url)
    if not m3u:
        return None
    fd = open(m3u, 'r')
    for l in fd.readlines():
        lists.append(l.rstrip('\n'))
    fd.close()
    return lists

def extractSUB(url):

    if not url or not re.search(r'youtube.com', url):
        return None

    print('\n[ytdl][extracSUB]\n')
    print('\turl: '+url)

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
        print('\tret: exception')
        return None

    m = re.search(r'Writing video subtitles to: (.*)', output)
    if m:
        local = m.group(1)
        print('\tsub: '+local)
        return local

    return None

